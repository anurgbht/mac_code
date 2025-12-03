## Univariate Report
import os
def univariate_report(df,  col_type='number'):
	univariate(df,'category').to_csv('univariate_category.csv')
	univariate(df,'number').to_csv('univariate_number.csv')
	univariate(df,'datetime').to_csv('univariate_datetime.csv')
	print('Reports are generated - '+os.getcwd())
	print([x for x in os.listdir() if 'univariate_' in x])
	
def univariate(df, col_type='number'):
    
    rows = df.shape[0]    
    descr = df.describe(include=[col_type]) 
    
    missing = rows - descr.loc['count', :]
    missing.name = 'missing'

    pct_missing = (rows - descr.loc['count',:])/rows
    pct_missing.name = 'missing%'
    
    descr = descr.append([missing, pct_missing])
    
    ## Numerical type    
    if col_type=='number':
        descr = descr.reindex(['count','missing','missing%','mean','std','min','25%','50%','75%','max'])
        
    ## Object and Category type
    elif col_type in ['O', 'category']:
        top5_list = []
        for col in descr.columns:
            top5 = df[col].value_counts().head().to_dict()
            top5_list.append(str(top5))
        top5 = pd.Series(top5_list, index=descr.columns)
        top5.name = 'top5'
        descr = descr.append(top5)
        descr = descr.reindex(['count','missing','missing%','unique','top5'])
        
    ## Datetime type
    elif col_type=='datetime':
        descr = descr.reindex(['count','missing','missing%','unique','first','last'])   
    return descr













