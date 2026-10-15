import base64,csv,io,json,re,zlib
from decimal import Decimal
from pathlib import Path

root=Path(__file__).parent
model=json.loads((root/'Banking.SemanticModel/model.bim').read_text())['model']
data={}
for table in model['tables']:
    if table['partitions'][0]['source']['type']!='m':continue
    source_expression=table['partitions'][0]['source']['expression']
    expression='\n'.join(source_expression) if isinstance(source_expression,list) else source_expression
    encoded=re.search(r'Binary.FromText\("([A-Za-z0-9+/=]+)"',expression).group(1)
    compressed=base64.b64decode(encoded)
    try: raw=zlib.decompress(compressed)
    except zlib.error: raw=zlib.decompress(compressed,-15)
    rows=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
    assert rows,table['name']
    assert set(c['sourceColumn'] for c in table['columns'])<=set(rows[0]),table['name']
    data[table['name']]=rows
for r in model['relationships']:
    if r['fromTable'] not in data or r['toTable'] not in data:continue
    dimension=data[r['toTable']]
    keys=[x[r['toColumn']] for x in dimension]
    assert len(keys)==len(set(keys)),r['toTable']
    keyset=set(keys)
    assert all(x[r['fromColumn']] in keyset for x in data[r['fromTable']]),r['name']
    assert r.get('crossFilteringBehavior','oneDirection')=='oneDirection'
tx=data['Transactions'];customers=data['Customers'];accounts=data['Accounts']
metrics={
 'bank_revenue_cad':float(sum(Decimal(x['bank_revenue']) for x in tx)),
 'transactions':len(tx), 'customers':len(customers),
 'active_customers':sum(x['customer_status']=='Active' for x in customers),
 'inactive_rate':sum(x['customer_status']=='Inactive' for x in customers)/len(customers),
 'digital_share':sum(int(x['is_digital'])==1 for x in tx)/len(tx),
 'products_per_customer':len(accounts)/len(customers)}
expected={'bank_revenue_cad':3911430.27,'transactions':250000,'customers':25000,'active_customers':20233,'inactive_rate':.19068,'digital_share':.69616,'products_per_customer':2.8238}
for name,val in expected.items(): assert abs(metrics[name]-val)<.00001,(name,metrics[name],val)
tables={t['name']:t for t in model['tables']}
pages=list((root/'Banking.Report/definition/pages').glob('*/page.json'))
visuals=list((root/'Banking.Report/definition/pages').glob('*/visuals/*/visual.json'))
for visual in visuals:
    v=json.loads(visual.read_text())
    for match in re.finditer(r'"Entity":\s*"([^"]+)"',json.dumps(v)): assert match.group(1) in tables
    def check_fields(obj):
        if isinstance(obj,dict):
            for kind in ['Measure','Column']:
                if kind in obj:
                    fld=obj[kind];entity=fld['Expression']['SourceRef']['Entity']
                    names=[x['name'] for x in tables[entity]['measures' if kind=='Measure' else 'columns']]
                    assert fld['Property'] in names,(visual,fld)
            for child in obj.values():check_fields(child)
        elif isinstance(obj,list):
            for child in obj:check_fields(child)
    check_fields(v)
    pos=v['position'];p=json.loads(visual.parents[2].joinpath('page.json').read_text())
    assert pos['x']>=0 and pos['y']>=0 and pos['x']+pos['width']<=p['width'] and pos['y']+pos['height']<=p['height'],visual
result={'status':'source_and_embedded_data_checks_passed','native_powerbi_validation':'not_executed_by_this_script','scope':'Python reconciliation of embedded CSV snapshots and structural references; does not execute DAX/M or render Power BI. Native Desktop evidence is recorded separately in validation_results.json. Desktop-generated hidden date tables are excluded from CSV checks.','tables':{k:len(v) for k,v in data.items()},'relationships':sum(r['fromTable'] in data and r['toTable'] in data for r in model['relationships']),'pages':len(pages),'visuals':len(visuals),'measures':sum(len(t.get('measures',[])) for t in model['tables']),'metrics':metrics}
(root/'source_validation_results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))