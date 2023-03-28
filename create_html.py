import modin.pandas as pd

df1 = pd.read_csv('states.csv')
df2 = pd.read_csv('temple_details.csv')

df1 = df1.loc[df1['state']=='Karnataka']

html = '''<!DOCTYPE html>
<html>
<head>
  <title>Indian Temples</title>
</head>
<body>
'''

for index,row in df1.iterrows():
    print(row['state'])
    html += f"<h2>{row['state']}</h2>\n"
    html += f"<p>{row['description']}</p>\n"
    df3 = df2.loc[df2['state']==row['state']]
    for index2, row2 in df3.iterrows():
        print(row2['temple_name'])
        html += f"<h3>{row2['temple_name']}</h3>\n"
        html += f"<p>{row2['temple_details']}</p>\n"

html += '''
</body>
</html>
'''

with open('temple_details_ka.html', 'w') as f:
    f.write(html)
