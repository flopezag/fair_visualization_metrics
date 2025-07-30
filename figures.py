import matplotlib.pyplot as plt
from analysis.graphics import Graphics
from analysis.data import Data


def example_data():
    data = {
        'Findable': {
            'labels': ['RDA-F1-01M', 'RDA-F1-01D', 'RDA-F1-02M', 'RDA-F1-02D', 'RDA-F2-01M', 'RDA-F3-01M',
                       'RDA-F4-01M'],
            'data': [1, 2, 3, 4, 1, 2, 3]
        },
        'Accessible': {
            'labels': ['RDA-A1-01M', 'RDA-A1-02M', 'RDA-A1-02D', 'RDA-A1-03M', 'RDA-A1-03D', 'RDA-A1-04M',
                       'RDA-A1-04D', 'RDA-A1-05D', 'RDA-A1.1-01M', 'RDA-A1.1-01D', 'RDA-A1.2-01D', 'RDA-A2-01M'],
            'data': [1, 2, 3, 4, 5, 2, 3, 4, 3, 2, 1, 1]
        },
        'Interoperable': {
            'labels': ['RDA-I1-01M', 'RDA-I1-01D', 'RDA-I1-02M', 'RDA-I1-02D', 'RDA-I2-01M', 'RDA-I2-01D',
                       'RDA-I3-01M', 'RDA-I3-01D', 'RDA-I3-02M', 'RDA-I3-02D', 'RDA-I3-03M', 'RDA-I3-04M'],
            'data': [1, 2, 3, 4, 5, 2, 3, 3, 1, 2, 1, 5]
        },
        'Reusable': {
            'labels': ['RDA-R1-01M', 'RDA-R1.1-01M', 'RDA-R1.1-02M', 'RDA-R1.1-03M', 'RDA-R1.2-01M',
                       'RDA-R1.2-02M', 'RDA-R1.3-01M', 'RDA-R1.3-01D', 'RDA-R1.3-02M', 'RDA-R1.3-02D'],
            'data': [1, 2, 3, 4, 5, 2, 3, 1, 1, 2]
        }
    }

    return data


if __name__ == '__main__':
    
    save_images = True
    
    #data = example_data()
    data = Data(json_file="example.json")
    data2 = Data(json_file="example_new.json")  # set to None if using only one data source
    
    # data names are used only when both data sources are given and 
    # are used in graph titles, so there is no need to adjust them 
    # for single data source functionality 
    data_name = "WFIPv2"
    data_name2 = "WFIPv3"
    
    
    gph = Graphics(data=data, 
                   data2=data2,
                   data_name=data_name,
                   data_name2=data_name2)

    gph.create_first_figure(category=None) # this is for MELODA5

    gph.create_first_figure(category='Findable')
    gph.create_first_figure(category='Accessible')
    gph.create_first_figure(category='Interoperable')
    gph.create_first_figure(category='Reusable')

    gph.create_second_figure(model_type="FAIR")
    gph.create_second_figure(model_type="MQA")

    gph.pie_chart(data)
    
    #if data2 is not None:
    #    gph.pie_chart(data2, data_name2)

    #gph.cumulative_proportion_bar_chart()
    
    # Save all open figures
    if save_images:
        for i, fig_num in enumerate(plt.get_fignums()):
            fig = plt.figure(fig_num)
            fig.savefig(f"figure_{i}.png", dpi=300, bbox_inches='tight')

    # Show them (optional, if you still want to view)
    plt.show()
