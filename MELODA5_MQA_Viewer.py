"""
This code can be used for visualising MELODA5 and MQA data from the JSON files
that were produced via the WFIP questionaire.

The code will generate radar plots for either MELODA5 or MQA responses in WFIP questionaire
"""

from json import load
import plotly.express as px
import pandas as pd
def Define_MQA_Scores():

    #color_labels = ['Not FAIR', 'FAIR Essential criteria only', 'FAIR Essential criteria + 50% of important criteria', 
            #'FAIR Essential criteria + 100% of important criteria', 'FAIR Essential criteria + 100% of important criteria + 50% of useful criteria', 
            #'FAIR Essential criteria + 100% of important criteria + 100% of useful criteria']
    #Create dictionary for MQA that links the MQA ID with respective catergory
    #intialise each to have a value of zero (0 corresponds to No as default response')
    mqa_scores = {}
    mqa_scores['Findability'] = {}
    mqa_scores['Findability']['MQAF1'] = 30.0
    mqa_scores['Findability']['MQAF2'] = 30.0
    mqa_scores['Findability']['MQAF3'] = 20.0
    mqa_scores['Findability']['MQAF4'] = 20.0 #100 total

    mqa_scores['Accessibility'] = {}
    mqa_scores['Accessibility']['MQAA1'] = 50.0
    mqa_scores['Accessibility']['MQAA2'] = 20.0
    mqa_scores['Accessibility']['MQAA3'] = 30.0 #100 total

    mqa_scores['Interoperability'] = {}
    mqa_scores['Interoperability']['MQAI1'] = 20.0
    mqa_scores['Interoperability']['MQAI2'] = 10.0
    mqa_scores['Interoperability']['MQAI3'] = 10.0
    mqa_scores['Interoperability']['MQAI4'] = 20.0
    mqa_scores['Interoperability']['MQAI5'] = 20.0
    mqa_scores['Interoperability']['MQAI6'] = 30.0 #110 total

    mqa_scores['Reusability'] = {}
    mqa_scores['Reusability']['MQAR1'] = 20.0
    mqa_scores['Reusability']['MQAR2'] = 10.0
    mqa_scores['Reusability']['MQAR3'] = 10.0
    mqa_scores['Reusability']['MQAR4'] = 5.0
    mqa_scores['Reusability']['MQAR5'] = 20.0
    mqa_scores['Reusability']['MQAR6'] = 10.0 #75 total
 
    mqa_scores['Contextuality'] = {}
    mqa_scores['Contextuality']['MQAC1'] = 5.0
    mqa_scores['Contextuality']['MQAC2'] = 6.0
    mqa_scores['Contextuality']['MQAC3'] = 7.0
    mqa_scores['Contextuality']['MQAC4'] = 8.0 #26 total

    return mqa_scores

def Define_MELODA_Scores():

    #Using scorig system for each catagory from https://www.meloda.org/ for reference. Define score values to
    #each question from WFIP that refers to MELODA5

    meloda_scores = {}
    meloda_scores['MELODA1'] = {}
    meloda_scores['MELODA2'] = {}
    meloda_scores['MELODA3'] = {}
    meloda_scores['MELODA4'] = {}
    meloda_scores['MELODA5'] = {}
    meloda_scores['MELODA6'] = {}
    meloda_scores['MELODA7'] = {}
    meloda_scores['MELODA8'] = {}

    meloda_scores['MELODA1']['Private use'] = 1
    meloda_scores['MELODA1']['Non-commercial reuse'] = 3
    meloda_scores['MELODA1']['Commercial reuse or no restrictions'] = 6

    meloda_scores['MELODA2']['Web access or unique URL parameters to dataset'] = 1
    meloda_scores['MELODA2']['Web Access unique with parameters to single data'] = 3 
    meloda_scores['MELODA2']['API or query language'] = 6

    meloda_scores['MELODA3']['Closed standard reusable and open non reusable'] = 1
    meloda_scores['MELODA3']['Open standard reusable'] = 3
    meloda_scores['MELODA3']['Open standard, individual metadata'] = 6

    meloda_scores['MELODA4']['Own data model standardization'] = 1
    meloda_scores['MELODA4']['Own ad hoc data model standardization published (harmonization)'] = 3
    meloda_scores['MELODA4']['Local standardization'] = 6
    meloda_scores['MELODA4']['Global standardization'] = 10

    meloda_scores['MELODA5']['No geographic information'] = 1 
    meloda_scores['MELODA5']['Simple or complex text field'] = 3
    meloda_scores['MELODA5']['Coordinates or full geographical information'] = 6

    meloda_scores['MELODA6']['Longer than 1 month'] = 1
    meloda_scores['MELODA6']['Monthly. Updating period ranges from 1 month to 1 day'] = 3
    meloda_scores['MELODA6']['Daily. Updating period ranges from 1 day to 1 hour'] = 6
    meloda_scores['MELODA6']['Hour. Updating period ranges from 1 hour to 1 minute'] = 10 
    meloda_scores['MELODA6']['Seconds. Updating period is lower than 1 minute'] = 15

    meloda_scores['MELODA7']['No information about the reputation of the data source'] = 1
    meloda_scores['MELODA7']['Statistics or reports published on users opinions'] = 3
    meloda_scores['MELODA7']['Indicators or rankings on reputation of the data source'] = 6

    meloda_scores['MELODA8']['Communication / dissemination not systematic'] = 1
    meloda_scores['MELODA8']['Available resources on updates (i.e., RSS feed)'] = 3
    meloda_scores['MELODA8']['Proactive dissemination / push dissemination (information automatic and timely)'] = 6

    return meloda_scores

def Map_MELODA_Scores(data,meloda_scores):

    #Create dictionary from mapping JSON keys to MELODA5 categories
    meloda_model = {
        'MELODA1': 'License of data set',
        'MELODA2': 'Access to data',
        'MELODA3': 'Technical standard',
        'MELODA4': 'Standardization',
        'MELODA5': 'Geolocation content',
        'MELODA6': 'Updating frequency',
        'MELODA7': 'Reputation',
        'MELODA8': 'Dissemination'
    }

    meloda_model_data = {}

    # Precompute max values for each meloda_model[key] for later use in normalisation of results
    max_values = {key: max(meloda_scores[key].values()) for key in meloda_model}

    # Iterate over keys in meloda_model
    for key in meloda_model:
        # Calculate the rounded normalised score for each category from the WFIP questionaire store it in meloda_model_data
        meloda_model_data[meloda_model[key]] = round(meloda_scores[key][data['responses'][0][key]] / max_values[key], 2)
   
    old_model_data = {}
    old_model_data['License of data set'] = 1.0 / max_values['MELODA1']
    old_model_data['Access to data'] = 6.0 / max_values['MELODA2']
    old_model_data['Technical standard'] = 6.0 / max_values['MELODA3']
    old_model_data['Standardization'] = 1.0 / max_values['MELODA4']
    old_model_data['Geolocation content'] = 6.0 / max_values['MELODA5']
    old_model_data['Updating frequency'] = 6.0 / max_values['MELODA6']
    old_model_data['Reputation'] = 1.0 / max_values['MELODA7']
    old_model_data['Dissemination'] = 1.0/ max_values['MELODA8']

    return old_model_data#meloda_model_data

def Map_MQA_Scores(data,mqa_scores):

    max_score = {}
    max_score['Findability'] = 100
    max_score['Accessibility'] = 100
    max_score['Interoperability'] = 110
    max_score['Reusability'] = 75
    max_score['Contextuality'] = 26

    Total_MQA_Points = 0.0
    mqa_model_data = {}
    normalised_mqa_model_data = {}

    #Loop through each MQA category Findability, Accessibility, etc...
    for catagory in mqa_scores.keys():
        score_value = 0.0
        check_count = 0.0
        val = "No"
        #Loop through each question in each category
        for question in mqa_scores[catagory].keys():
            #Count number of questions asked
            check_count += 1.0
            #Get resonse to question
            val = data['responses'][0][question]
            #Count number of positive "Yes" responses for each category
            if val == 'Yes':
                score_value += mqa_scores[catagory][question]
        
        #Create normalised value for yes reponses
        #normnlised value = number of yes responses in category / number of questions asked in category
        #val = round((score_value/check_count),2)
        mqa_model_data[catagory] = score_value
        normalised_mqa_model_data[catagory] = score_value/max_score[catagory]
        Total_MQA_Points += score_value

    return mqa_model_data, normalised_mqa_model_data, Total_MQA_Points


def Data(json_file):

    #Read JSON file
    with open(file=json_file, mode='r') as f:
        raw_data = load(f)

    return raw_data

def plot_data(model_data,normalised_model_data,output_file,plot_title,total_score,normalised):
    
    #Chooses color of plot based on whether MELODA5 or MQA data
    if plot_title == 'MELODA5':
        plot_colour = ['green']
        #Get the labels for each category of radar plot
        labels = list(model_data.keys())
        #Get values for each category of radar plot
        case_data = list(model_data.values())

        #This code creates the ticks/scale bar frrom 0 to 1 at 0.2 intervals
        tickvals = [i / 5 for i in range(11)]

        #Draw radar plot
        fig = px.line_polar( 
                r=case_data,
                theta=labels,
                line_close=True,
                range_r=[0,1],
                color_discrete_sequence=plot_colour#['red']  # Set the color to green
                
            )
            
        fig.update_traces(fill='toself')
        fig.update_polars(radialaxis=dict({
            #'gridcolor': 'grey',
            'linecolor': 'grey',
            'linewidth': 0.5,
            'color': 'black',
            'tickcolor': 'black'
            }
        ))

        fig.update_layout(
                title={
                'text': '<b>' + str(plot_title) + '</b>',
                'y': 0.99,  # Adjust the y-coordinate for vertical alignment
                'x': 0.5,  # Adjust the x-coordinate for horizontal alignment
                'xanchor': 'center',  # Anchor the title to the center horizontally
                'yanchor': 'top',  # Anchor the title to the top vertically
                'font': {'size': 20, 'color': 'black'}
                },

            polar=dict(
                radialaxis=dict(
                    visible=True,
                    tickvals=tickvals,  # Specify the integer values for the ticks
                    tickmode='array',  # Use the specified tick values
                    dtick=1,  # Set the tick interval to 1
                    tickfont=dict(size=14),  # Adjust font size of tick numbers
                    tickangle=0,  # Keep tick numbers horizontal
                    linecolor='black'
                    
                ),
                angularaxis=dict( 
                tickfont = {
                    'size': 16
                }
                )   
            ),
            showlegend=False
        )
    else:

        if normalised == 0:
            # Create a DataFrame from the dictionary
            df = pd.DataFrame({'Category': list(model_data.keys()), 'Value': list(model_data.values())})

            # Plotting
            fig = px.bar(df, x='Category', y='Value', color='Category', labels={'Category': 'MQA Categories', 'Value': 'MQA Score'})
            # Hide legend
            fig.update_traces(showlegend=False)
            fig.update_layout(
                    title={
                    'text': '<b>MQA Total Score = ' + str(int(total_score)) + '</b>',
                    'y': 0.99,  # Adjust the y-coordinate for vertical alignment
                    'x': 0.5,  # Adjust the x-coordinate for horizontal alignment
                    'xanchor': 'center',  # Anchor the title to the center horizontally
                    'yanchor': 'top',  # Anchor the title to the top vertically
                    'font': {'size': 20, 'color': 'black'}
                    })
        else:
             # Create a DataFrame from the dictionary
            df = pd.DataFrame({'Category': list(normalised_model_data.keys()), 'Value': list(normalised_model_data.values())})

            # Plotting
            fig = px.bar(df, x='Category', y='Value', color='Category', labels={'Category': 'MQA Categories', 'Value': 'MQA Score'})
            # Hide legend
            fig.update_traces(showlegend=False)
            fig.update_layout(
                    title={
                    'text': '<b>Normalised MQA Scores</b>',
                    'y': 0.99,  # Adjust the y-coordinate for vertical alignment
                    'x': 0.5,  # Adjust the x-coordinate for horizontal alignment
                    'xanchor': 'center',  # Anchor the title to the center horizontally
                    'yanchor': 'top',  # Anchor the title to the top vertically
                    'font': {'size': 20, 'color': 'black'}
                    })
            # Specify the range of y-axis
            fig.update_yaxes(range=[0, 1.0])
        #fig.update_layout(title='<b>MQA Score</b>')
    
    #This code writes the plot from plotly to user specified file using kaleido
    fig.write_image(output_file, engine="kaleido")

    return

if __name__ == '__main__':

    #Write the location and filename of your json file here
    json_file = r'C:\Waterverse\input_data\sww.json'

    #Choose what data you wish to plot either MELODA5 or MQA
    plot_type = 'MELODA5' #'MQA' 'MELODA5'
    
    #Write location and filename of your output here as *.png file e.g. C:\MyDocuments\sww_meloda5.png
    output_file = r'C:\Myoutputs\MyMELODA5.png'

    #This option used for creating MQA charts either with numerical scores or normalised scores
    normalised = 1 #Set to 0 for normal scoring or 1 for normalised

    """*** -----Do not change code beneath this line----- unless you want to :D ***"""
    
    #Read JSON file
    data = Data(json_file)

    #Generate plots
    if plot_type == 'MELODA5':
        #Create lookup tables
        meloda_scores = Define_MELODA_Scores()
        #Map data from quesionaire to python dictionary
        meloda_model_data = Map_MELODA_Scores(data, meloda_scores)
        #Plot data as radar chart
        plot_data(meloda_model_data,'',output_file,'MELODA5',0.0,normalised)
    else:
        #Create lookup tables
        mqa_scores = Define_MQA_Scores()
        #Map data from quesionaire to python dictionary
        mqa_model_data, normalised_mqa_model_data, Total_MQA_Points = Map_MQA_Scores(data,mqa_scores)
        #Plot data as radar chart
        plot_data(mqa_model_data,normalised_mqa_model_data,output_file,'MQA',Total_MQA_Points,normalised)
    