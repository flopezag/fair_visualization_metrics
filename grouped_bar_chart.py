import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.colors import to_rgb
from analysis.data import Data

def change_MELODA_names(meloda_data):
    new_data = {}
    for pilot, data in meloda_data.items():
        new_data[pilot] = {}
        for i, (_, value) in enumerate(data.items()):
            new_data[pilot][f"MELODA{i+1}"] = value
    return new_data

def darken_color(color, amount=0.8):
    """Darken a matplotlib color by a given factor (0–1)."""
    r, g, b = to_rgb(color)
    return (r * amount, g * amount, b * amount)


def brighten_color(color, amount=0.6):
    """
    Brighten a matplotlib color by blending it with white.
    amount: 0 (no change) to 1 (fully white)
    """
    r, g, b = to_rgb(color)
    return (r + (1 - r) * amount,
            g + (1 - g) * amount,
            b + (1 - b) * amount)


def grouped_bar_chart(data_old, data_new=None, grouping="pilot", model_data="MQA"):

    # Convert to DataFrame
    df = pd.DataFrame(data_old).T
    if data_new != None:
        df_new = pd.DataFrame(data_new).T
    else:
        df_new = df

    bar_width = 0.7
    
    # grouping by pilot
    if grouping == "pilot":
        index = df.index
        columns = df.columns
        columns_new = df_new.columns
        
    # grouping by measure
    elif grouping == "measure":
        index = df.columns
        columns = df.index
        columns_new = df_new.index
        df_new = df_new.loc
        df = df.loc
    else:
        raise Exception("please select grouping by 'pilot' or by 'meausre'.")
    
    x = np.arange(len(index))

    fig, ax = plt.subplots(figsize=(10, 6))

    alpha_new = 0.9
    color_new = 0.1
    # # Plot new dataset (transparent overlay)
    for i, col in enumerate(columns_new):
        ax.bar(x - bar_width/2.5 + i*bar_width/len(columns_new), df_new[col],
            width=bar_width/len(columns_new), 
            color=brighten_color(f"C{i}", amount=color_new), 
            #edgecolor=darken_color(f"C{i}"),  # <-- darker hatch color
            #hatch='///',                      # diagonal stripes
            alpha=alpha_new)

    if data_new != None:
        alpha=0.8
        color_old = 0.85
        # # Plot old dataset
        for i, col in enumerate(columns):
            ax.bar(x - bar_width/2.5 + i*bar_width/len(columns), df[col], 
                width=bar_width/len(columns), 
                color='none',
                edgecolor=darken_color(f"C{i}", amount=color_old),  # <-- darker hatch color
                hatch='///',                      # diagonal stripes
                label=col, 
                alpha=alpha)

    # Plotting
    #ax = df.plot(kind='bar', figsize=(10, 6))
    #ax.set_xticks(range(len(index)))  # positions

    ax.set_xticks(x)
    ax.set_xticklabels(index, rotation=0)  # now metrics are on x-axis

    ax.set_title(f"{model_data} score per {grouping}")
    ax.set_ylabel("Score")
    ax.set_xticks(range(len(index)))  # positions
    ax.set_xticklabels(index, rotation=0)  # labels
    ax.axis('on')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    for i in range(0, 12, 2):
        ax.axhline(i/10, color='grey', alpha=0.2, lw=1)
        
        # Custom legend handles
    handles = []
    for i, col in enumerate(columns):
        if data_new != None:
            solid_patch = mpatches.Patch(color=brighten_color(f"C{i}", amount=color_new), label=f"{col} (new)", alpha=alpha_new)
            hatch_patch = mpatches.Patch(facecolor='none',
                                        edgecolor=darken_color(f"C{i}", amount=0.85),  # <-- darker hatch color
                                        hatch='///',
                                        alpha=alpha,
                                        label=f"{col} (old)")
            handles.append(solid_patch)
            handles.append(hatch_patch)
        else:
            solid_patch = mpatches.Patch(color=brighten_color(f"C{i}", amount=color_new), label=f"{col}", alpha=alpha_new)
            handles.append(solid_patch)
            
    ax.legend(
        handles=handles,
        title="",
        loc='upper center',
        bbox_to_anchor=(0.5, -0.15),
        ncol=len(columns),
        frameon=False
    )
    plt.tight_layout()



if __name__ == '__main__':
    
    save_images = True
    #HIDR -> ES Pilot
    #HST -> DE Pilot
    #KEYPRO -> FI Pilot
    #PWN -> NE Pilot
    #SWW -> UK Pilot
    #WBL -> CY Pilot
    
    data_old_mqa = {
        "es pilot": Data(json_file="hidr.json").mqa_model_data,
        "de pilot": Data(json_file="hst.json").mqa_model_data,
        "fi pilot": Data(json_file="keypro.json").mqa_model_data,
        "ne pilot": Data(json_file="pwn.json").mqa_model_data,
        "uk pilot": Data(json_file="sww.json").mqa_model_data,
        "cy pilot": Data(json_file="wbl.json").mqa_model_data,
    }
    
    data_new_mqa = {
        "es pilot": Data(json_file="hidr.json").mqa_model_data,
        "de pilot": Data(json_file="hst.json").mqa_model_data,
        "fi pilot": Data(json_file="keypro.json").mqa_model_data,
        "ne pilot": Data(json_file="pwn.json").mqa_model_data,
        "uk pilot": Data(json_file="sww.json").mqa_model_data,
        "cy pilot": Data(json_file="wbl.json").mqa_model_data,
    }
    data_new_mqa = None
    mqa = grouped_bar_chart(data_old_mqa, data_new_mqa, grouping="pilot", model_data="MQA")
        
    data_old_meloda = {
        "es pilot": Data(json_file="hidr.json").meloda_model_data,
        "de pilot": Data(json_file="hst.json").meloda_model_data,
        "fi pilot": Data(json_file="keypro.json").meloda_model_data,
        "ne pilot": Data(json_file="pwn.json").meloda_model_data,
        "uk pilot": Data(json_file="sww.json").meloda_model_data,
        "cy pilot": Data(json_file="wbl.json").meloda_model_data,
    }
    
    data_new_meloda = {
        "es pilot": Data(json_file="hidr.json").meloda_model_data,
        "de pilot": Data(json_file="hst.json").meloda_model_data,
        "fi pilot": Data(json_file="keypro.json").meloda_model_data,
        "ne pilot": Data(json_file="pwn.json").meloda_model_data,
        "uk pilot": Data(json_file="sww.json").meloda_model_data,
        "cy pilot": Data(json_file="wbl.json").meloda_model_data,
    }
    
    data_old_meloda = change_MELODA_names(data_old_meloda)
    data_new_meloda = change_MELODA_names(data_new_meloda)
    data_new_meloda = None

    meloda = grouped_bar_chart(data_old_meloda, data_new_meloda, grouping="measure", model_data="MELODA5")

    if save_images:
        for i, fig_num in enumerate(plt.get_fignums()):
            fig = plt.figure(fig_num)
            fig.savefig(f"grouped_bar_chart_{i}.png", dpi=300, bbox_inches='tight')

    plt.show()
    
