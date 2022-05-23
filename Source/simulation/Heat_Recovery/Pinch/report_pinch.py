import pandas as pd
import matplotlib.pyplot as plt, mpld3
import os

def make_pretty(styler):
    styler.background_gradient(axis=None, vmin=1, vmax=5, cmap="YlGnBu")
    return styler

 #################################################################
# STYLING
cell_hover = {  # for row hover use <tr> instead of <td>
        'selector': 'td:hover',
        'props': [('background-color', '#c4a5a7')]
    }

row_hover = {  # for row hover use <tr> instead of <td>
        'selector': 'tr:hover',
        'props': [('background-color', '#c4a5a7')]
    }

mai = {
        'selector': 'th:hover',
        'props': 'background-color: #c4a5a7; color: white;'
    }

new = {
        'selector': 'td:.index_name',
        'props': 'background-color: #ffffff; color: black;'
    }

headers = {
        'selector': 'th:.Fluid',
        'props': 'background-color: #e27a53; color: white;'
    }

text_aligned = { 'selector': 'td',
                     'props': 'text-align: center; '
    }


index_names = {
    'selector': '.index_name',
    'props': 'font-style: italic; color: darkgrey; font-weight:normal;'
}

def report_pinch(df,fig_html, type, solution_order,stream_table,stream_combination_not_feasible,df_solutions):

    #################################################################

    # DEF VARS
    df.index.name = 'HX ID'
    df_overview = df[['Total_Turnkey_Cost','Recovered_Energy','Storage_Turnkey_Cost']]
    df_hx = df[['HX_Power', 'HX_Original_Cold_Stream', 'HX_Original_Hot_Stream', 'HX_Hot_Stream_T_Hot', 'HX_Hot_Stream_T_Cold','HX_Hot_Stream', 'HX_Cold_Stream', 'HX_Hot_Stream_mcp', 'HX_Cold_Stream_mcp']]
    df_hx_economic = df[['HX_Type', 'HX_Turnkey_Cost', 'HX_OM_Fix_Cost']]
    df_storage = df[['Storage', 'Storage_Satisfies', 'Storage_Turnkey_Cost']]


    # rearrange df_hx data for visualization
    df_hx = df[["HX_Power","HX_Original_Cold_Stream","HX_Cold_Stream_mcp","HX_Cold_Stream_T_Cold","HX_Cold_Stream_T_Hot",
                "HX_Original_Hot_Stream","HX_Hot_Stream_mcp","HX_Hot_Stream_T_Hot","HX_Hot_Stream_T_Cold"]]
    data = [df_hx.iloc[index].values for index in range(df_hx.shape[0])]
    cols = pd.MultiIndex.from_tuples([("","HX Power"),
                                      ("Cold Stream", "ID"),
                                      ("Cold Stream", "mc<sub>p</sub>"),
                                      ("Cold Stream", "T<sub>in</sub>"),
                                      ("Cold Stream", "T<sub>out</sub>"),
                                      ("Hot Stream", "ID"),
                                      ("Hot Stream", "mc<sub>p</sub>"),
                                      ("Hot Stream", "T<sub>in</sub>"),
                                      ("Hot Stream", "T<sub>out</sub>"),
                                      ])

    index = df_hx.index

    df_hx = pd.DataFrame(data, columns=cols,index=index,)
    df_hx = df_hx.style.format('{:.0f}')
    df_hx_economic = df_hx_economic.style
    df_storage = df_storage.style.format('{:.0f}')
    df_overview = df_overview.style.format('{:.0f}')
    stream_table = stream_table.style
    df_solutions = df_solutions.style

    df_hx = df_hx.set_properties(**{'width': '100px'})
    #df_hx_economic = df_hx_economic.set_properties(**{'width': '150px'})

    df_storage = df_storage.set_properties(**{'width': '150px'})
    df_overview = df_overview.set_properties(**{'width': '200px'})
    stream_table = stream_table.set_properties(**{'width': '200px'})

    df_hx = df_hx.set_table_styles([row_hover])
    df_hx_economic = df_hx_economic.set_table_styles([row_hover])
    df_storage = df_storage.set_table_styles([row_hover])
    df_overview = df_overview.set_table_styles([row_hover])
    stream_table = stream_table.set_table_styles([row_hover])


    subtitle = type + " (solution " + str(solution_order) + " of 3)"

    if stream_combination_not_feasible == []:
        stream_combination_not_feasible = 'NOTE: All streams combinations were analyzed.'
    else:
        stream_combination_not_feasible = 'NOTE: The following combination of streams simulation was infeasible:' + str(stream_combination_not_feasible)


    from pathlib import Path
    script_dir = os.path.dirname(__file__)
    style = Path(os.path.join(script_dir, "../assets/style.css")).read_text()


    html_df = f'''
        <html>
            <head>
                <title>{"HELP"}</title>
                <style>{style}</style>
            </head>
            <body >             
                <div class="embers_logo">
                    <img class="image" src="https://www.rhc-platform.org/content/uploads/psf_projects/emb3rs-emb3rs-logo2.jpg">
                </div>
                <div class="embers_circle">
                    <img class="image" src="https://www.emb3rs.eu/wp-content/uploads/2019/12/home-graphic.png">
                </div>
                <h5>{"- HELP MANUAL -"}</h5>           
                <h2>{"REPORT: Pinch Analysis"}</h2>      
                <div class="tips">
                    <h7>{"What is a Pinch Analysis?"}</h7>    
                    <p>{'In brief, the pinch analysis is a theoretical method that, based on fundamental thermodynamics, ' 
                       'analyzes the heat flow through the industry’s streams with the aim of recovering heat within those ' 
                       'streams by proposing a heat exchanger - HX - network. By reducing the energy needs, it also reduces costs and CO<sub>2</sub> emissions (for more information check EMB3Rs deliverable D.3.3).'}
                    </p>   
                    <h7>{"What can you obtain from the report?"}</h7>            
                    <p>{'The simulation assesses heat recovery alternatives within ' 
                        'the streams by performing a series of pinch analysis to the streams combinations. ' 
                        'The output of this routine is the 3 best pinch designs in terms of heat recovery (kW), lowest cost ' 
                        'of heat (€/MWh) and highest CO<sub>2</sub> emission reductions/savings (kgCO<sub>2</sub>/kWh). '}
                    </p>    
                    <h7>{"What is the report structure?"}</h7>            
                        <p>{'1) It is presented a table with the streams and the minimum heat exchangers &#916T, the user provided. Below the ' 
                            'streams table it the user knows whether all possbile combinations of streams were analyzed or not. If not' 
                            'the list of infeasible streams combinations is shown. <br>' 
                            '2) For each of the categories (heat recovery, cost of heat and CO<sub>2</sub> emissions savings) ' 
                            'the 3 best simulated solutions are shown to the user.'     
                            }
                        </p>        
                </div>  
            
                <h4>{'User Streams'}</h4>     
                <center>{stream_table.to_html()}</center>   
                <p><bold>{stream_combination_not_feasible}</bold></p>  
                
                <h4 id="co2_solutions">{"Designed Solutions"}</h4>     
                <h3><a href="#co2_solutions"><b>{"CO<sub>2</sub> Savings"}</b></a></h3>  
                  <div class="tips"> 
                        <p>{'Here you can find an overview on the best 3 designed solutions for:' }</p>
                        <ul class="ul_tips">
                            <li>{'Heat recovery, cost of heat and CO<sub>2</sub> emissions savings'}</li>   
                            <li>{'CO<sub>2</sub> emissions savings'}</li>
                            <li>{'Heat recovery over Capex '}</li>
                        </ul>       
                        <p>{'You can find for each designed solution the streams that were utilized, the Capex and the ' 
                            'energy, CO<sub>2</sub> and money savings. ' }</p>
                        <p><bold>{'For the three categories analyzed there can be repetition on the designed solutions - look at the ID. ' 
                                  'There will bea always Energy savings in all solutions, since the pinch analysis aims to recover energy. ' 
                                  'However, ther may not be Money/CO<sub>2</sub> Savings if only streams without an equipment and fuel associated are provided' }</bold></p>
                    </div>   
                <center>{df_solutions.to_html()}</center>                   
                      
         
                <div id="co2_solutions" class="solution">                                                    
                    <h3><b>{subtitle}</b></h3>   
                    <h4>{'Heat Exchangers Network Diagram'}</h4>      
                        <div class="tips">                          
                            <p>{'In this subsection it is provided an economic analysis on the designed heat exchangers:' }</p>   
                                <ul class="ul_tips">
                                    <li>{'The following diagram proposes a heat exchanger (HX) network for the streams given.'}</li>   
                                    <li>{'The streams are represented by the horizontal lines with the respective IDs next to them.'}</li>   
                                    <li>{'Red lines mean hot streams, which are stream going from a larger to a smaller temperature. The opposite occurs to the blue lines, known as cold streams'}</li>   
                                    <li>{'Stream split may occur. This is to guarantee the achievement of a final solution. The splits are represented as the diagonal lines going out of the main/original stream.'}</li>   
                                    <li>{'The heat exchangers designed are represented with its ID, together with the estiamted power. In some cases a temperature may appear next to the HX, representing the temperature the stream reached. If not, it means it reached the target or the pinch temperature.'}</li>   
                                </ul>  
                        </div>       

                    <div class="img">                         
                        <center>{fig_html}</center>     
                    </div>    
                    
                    <h4>{'Solution Economic Data Overview'}</h4>
                    <div class="tips"> 
                        <p>{'In this subsection it is provided an overview of the most relevant tecno-economic parameters analized:' }</p>
                        <ul class="ul_tips">
                            <li>{'HX and storage turnkey - equipment investment cost'}</li>   
                            <li>{'Energy recovered - yearly amount of recovered energy'}</li>
                            <li>{'CO<sub>2</sub> emissions - '}</li>
                        </ul>       
                    </div>                          
                    <center> {df_overview.to_html()} </center>                                
                    <h4>{'Heat Exchangers Technical Data'}</h4>
                    <div class="tips"> 
                        <p>{'In this subsection it is provided an extensive technical analysis on the designed heat exchangers:' }</p>
                        <ul class="ul_tips">
                            <li>{'Power'}</li>                   
                            <li>{'Hot/Cold Stream data:'}</li>
                                <ul> 
                                <li> {'Hot Temperature (hot stream inlet or cold stream outlet)'}</li>  
                                <li> {'Cold Temperature (hot stream outlet or cold stream inlet)'}</li>  
                                <li> {'mcp - Heat Capacity'}</li>  
                                <li> {'Split - whether it is a split from the main stream or not  '}</li>  
                            </ul>             
                        </ul> 
                    </div>     
                    <center> {df_hx.to_html()}</center>        
                    <h4>{'HXs Estimated Economic Data'}</h4>
                    <div class="tips"> 
                        <p>{'In this subsection it is provided an economic analysis on the designed heat exchangers:' }</p>
                        <ul class="ul_tips">
                            <li>{'Power'}</li>   
                            <li>{'Cold data: ID, Hot (outlet) and cold (inlet) temperatures, the mcp, and wheter it is a split from the main stream or not.  '}</li>
                            <li>{'Hot Stream data: ID, Hot (inlet) and cold (outlet) temperatures, the mcp, and wheter it is a split from the main stream or not.'}</li>
                        </ul>  
                     </div>   
                    <center> {df_hx_economic.to_html()}</center>       
                    <h4>{'HXs Storage Estimated Data'}</h4>
                    <center> {df_storage.to_html()} </center>       
                </div>                     
            </body>
        </html>
    '''

    return html_df
