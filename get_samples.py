import pandas as pd

df = pd.read_csv('data/clean_earthquake_data.csv')
print('Alert distribution:', df['alert'].value_counts().to_dict())
print()

for alert in ['green', 'yellow', 'orange', 'red']:
    subset = df[df['alert'] == alert][['magnitude', 'depth', 'cdi', 'mmi', 'sig']]
    if not subset.empty:
        row = subset.iloc[0]
        print(f'--- {alert.upper()} sample ---')
        print(f'  magnitude={row.magnitude}, depth={row.depth}, cdi={row.cdi}, mmi={row.mmi}, sig={row.sig}')
