import plotly.graph_objects as go
import random


def sankeyPlot(title_text:str,df,source_column:str,target_column:str,aggregate_column:str,source_filter:list,target_filter:list,agg_func:str):
    """
    This will plot a sankey plot flow diagram between two_parts

    ---------
    Example
    ---------
    df = pd.read_csv("transactions_data.csv") ### df.columns = ['txn_id','country','sender_nat','reciever_nat','amount']
    source_filter = (True, ['OM',"US])
    target_filter = (False, [])
    agg_func = 'sum'
    _, fig = sankeyPlot("Skanky Diagram",df,'sender_nat','reciever_nat',aggregate_column,source_filter,target_filter,agg_func)
    fig.show()
    ---------
    INPUT
    ---------
    title_text = Title,
    df = takes pandas dataframe 
    source_column = any categorical column from the dataframe
    target_column = any categorical column from the dataframe 
    aggregate_column = any numerical column from the dataframe that you want to sum
    source_filter,target_filter = a tuple (Boolean , List), (True, ["Item 1", "Item 2]) or you don't need to use it (False, [])
    agg_func = only two values are accepted currently "sum" , "count"

    ---------
    OUTPUT
    ---------
    pivot = which is a dataframe that is used for the plotly sankey graph
    fig = a plotly figure
    """

    number_of_colors = 200
    
    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                for i in range(number_of_colors)]

    pivot = df.groupby([source_column,target_column]).agg([agg_func])[aggregate_column].reset_index()
    pivot.columns = ['sourceId','targetId',agg_func]

    pivot.sort_values(agg_func.lower(),inplace=True,ascending=False)

    sourceId_list = []
    for i in pivot['sourceId']:
        if i not in sourceId_list:
            sourceId_list.append(i)

    targetId_list = []
    for i in pivot['targetId']:
        if i not in targetId_list:
            targetId_list.append(i)

    if len(source_filter) != 0:
        pivot = pivot[pivot['sourceId'].isin(source_filter)] 
    
    if len(target_filter) != 0:
        pivot = pivot[pivot['targetId'].isin(target_filter)] 

    source_dict = {x:i for i,x in enumerate(sourceId_list)}
    target_dict = {x:i+len(sourceId_list) for i,x in enumerate(targetId_list)}

    labels = sourceId_list + targetId_list

    pivot['sourceId'] = [source_dict[x] for x in pivot['sourceId']]
    pivot['targetId'] = [target_dict[x] for x in pivot['targetId']]

    fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 10,
      line = dict(color = "black", width = 0.5),
      label = labels,
      color =  color[:len(sourceId_list)] + color[:len(targetId_list)]
    ),
    link = dict(
      source = pivot['sourceId'] ,
      target = pivot['targetId'] ,
      value = pivot[agg_func.lower()],
      color = color[:len(sourceId_list)] + color[:len(targetId_list)]
  ))  
        ])

    fig.update_layout(template='ggplot2',
                      title_text=title_text,
                      font_size=10,height=900)
    return pivot,fig