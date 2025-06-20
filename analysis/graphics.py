import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from analysis.radar import radar_factory
import numpy as np
from typing import Optional
from .data import Data
import textwrap
import math

class Graphics:
    def __init__(self, data: Data, 
                       data2: Optional[Data] = None,
                       data_name: Optional[str] = None,
                       data_name2: Optional[str] = None,
                       ):
        """
        Initializes the Graphics class for visualizing one or two datasets, 
        with optional naming for comparison purposes.

        Parameters:
        - data (Data): The primary dataset to be visualized.
        - data2 (Optional[Data]): A second dataset for comparison, if provided.
        - data_name (Optional[str]): A custom name for the primary dataset (used in legends/titles). 
                                    Defaults to the dataset's response_id.
        - data_name2 (Optional[str]): A custom name for the second dataset, if provided. 
                                    Defaults to the second dataset's response_id.
        
        Attributes:
        - self.data: Stores the primary dataset.
        - self.data2: Stores the second dataset for comparison (if provided).
        - self.overlay_plots: Boolean flag indicating if comparison plots should be generated.
        - self.data_name: Label name for the primary dataset.
        - self.data2_name: Label name for the second dataset.
        - self.cmap: A colormap from white to blue (Blues) for visual consistency in plots.
        """
        
        # primary data
        self.data = data
        
        # data for comparison
        self.data2 = data2
        
        # defining a flag to be used in functions later
        self.overlay_plots = data2 is not None
        
        # defining names for consistency between  different graphs
        # e.g. one name for one data source
        self.data_name = self.data.response_id if data_name is None else data_name
        self.data2_name = self.data2.response_id if data_name2 is None else data_name2
        
        # defining colors for consistency between graphs 
        # e.g. one color for one data source
        if self.overlay_plots:
            self.color1 = "grey"
            self.color2 = "blue"
        else:
            self.color1 = "blue"

        # Create the color map from white to blue
        self.cmap = plt.cm.get_cmap('Blues')

    def create_first_figure(self, category: str):
        theta = radar_factory(num_vars=len(self.data.fairness_classification_per_indicator[category]),
                              frame='polygon')
        
         # Get the lists with the data
        rda_labels = list(self.data.fairness_classification_per_indicator[category].keys())
        
        # maps from RDA codes to human readable labels
        long_labels = [self.data.rda_mapping[l] for l in rda_labels]
        
        # adds linebreaks to the labels for better readability on the graph
        labels = ['\n'.join(textwrap.wrap(label, width=30, 
                                    break_long_words=False, 
                                    break_on_hyphens=False))
                                    for label in long_labels]
        
        case_data = list(self.data.fairness_classification_per_indicator[category].values())

        # Create the first radar chart in Figure 1
        fig, ax = plt.subplots(figsize=(20, 12), subplot_kw=dict(projection='radar'))

        ax.set_title(label=f"{category}"+(f" {self.data_name} vs {self.data2_name}" if self.overlay_plots else ""),
                     horizontalalignment='center',
                     verticalalignment='top',
                     pad=80,
                     fontsize=24,
                     color=self.cmap(1.0), 
                     weight='semibold')
        
        # colors the axis of the spider/radar plot dark grey
        ax.xaxis.grid(True, color="dimgray")
        ax.yaxis.grid(True, color="dimgray")

        ax.plot(theta, case_data, color=self.color1, label=self.data_name if self.overlay_plots else None)
        ax.fill(theta, case_data, color=self.color1, alpha=0.25)
        
        if self.overlay_plots:
            case_data_2 = list(self.data2.fairness_classification_per_indicator[category].values())
            ax.plot(theta, case_data_2, color=self.color2, label=self.data2_name if self.overlay_plots else None)
            ax.fill(theta, case_data_2, color=self.color2, alpha=0.25)
        
        # Defined ticks for radar plot (5 is the max value for all radar plots)
        ax.set_yticks([1, 2, 3, 4, 5])  
        ax.set_varlabels(labels)
                
        def pull_towards_centers(angle_rad, strength=0.1):
            """
            ONLY VISUAL EFFECT, NO EFFECT ON DATA
            Pulls angle toward 90° if in [0, π), or toward 270° if in [π, 2π),
            with 0, π/2, π, and 3π/2 unchanged.

            Parameters:
                angle_rad (float): Angle in radians
                strength (float): How strongly to pull (0 = no pull, 1 = full snap)

            Returns:
                float: Adjusted angle in radians
            """
            angle_rad = angle_rad % (2 * math.pi)

            # Check for anchor angles: do not move them
            anchors = [0, math.pi/2, math.pi, 3*math.pi/2]
            for anchor in anchors:
                if abs(angle_rad - anchor) < 1e-6:
                    return angle_rad

            # Decide which direction to pull
            if 0 < angle_rad < math.pi:
                target = math.pi / 2  # pull toward 90°
            else:
                target = 3 * math.pi / 2  # pull toward 270°

            # Weighted average between angle and target
            return (1 - strength) * angle_rad + strength * target
                
        
        def radar_plot_text_displacement(angle_rad, max_disp=1.5):
            """
            ONLY VISUAL EFFECT, NO EFFECT ON DATA
            Calculate a radial text displacement factor for radar plot labels based on angle.

            This function is used to adjust the radial position of text labels in a radar (spider) plot,
            helping to prevent overlap by offsetting labels more strongly at horizontal angles (e.g., left/right)
            and less at vertical angles (e.g., top/bottom). The displacement is computed using the sine
            of the angle to achieve this effect.

            Parameters:
                angle_rad (float): The angle (in radians) for the label position on the radar plot.
                max_disp (float): The maximum displacement scaling factor (default is 1.5).

            Returns:
                float: A displacement value between 0 and `max_disp` to be added to the radius of the label.
            """
            # Normalize angle between 0 and 2π
            angle_rad = angle_rad % (2*math.pi)

            # Use absolute sine to get displacement between 0 and 1
            displacement_factor = abs(math.sin(angle_rad))

            # Scale by max displacement
            displacement = displacement_factor * max_disp
            
            return displacement

        # Define angles based on the number of labels
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)

        # Remove original x tick labels
        ax.set_xticklabels([])

        # Add custom labels
        for i, angle in enumerate(angles):
            adj_angle = pull_towards_centers(angle)  # your function
            disp = radar_plot_text_displacement(adj_angle)  # your radial offset

            ax.text(
                adj_angle,      # theta
                5.6 + disp,     # radius (adjust outward)
                labels[i],      # label text
                ha='center', va='center'
            )

        # Add legend
        if self.overlay_plots:
            ax.legend(
                loc="center right",
                bbox_to_anchor=(1, 0, 0.5, 1.3),
                fontsize=12)

        plt.tight_layout(rect=[0, 0, 1, 0.94])


    def create_second_figure(self):
        # Set the number of divisions in each column
        num_divisions = 6

        # Create the figure and axes
        fig, ax = plt.subplots(figsize=(13, 8))

        # Set the width of each column
        column_width = 0.6

        # Set the distance between the columns
        column_distance = 0.8

        # Color Value based on the number of divisions
        color_value = 0.0

        # Iterate over each column
        for i in range(4):
            # Calculate the x-coordinate of the column
            x = i * (column_width + column_distance)

            # Iterate over each division within the column
            for j in range(num_divisions):
                # Calculate the color value for the division
                color_value = j / (num_divisions - 1)

                # Get the color for the division using the color map
                color = self.cmap(color_value)

                # Plot the bar for the division
                ax.bar(x, 1, bottom=j, color=color, edgecolor='none', width=column_width)

        # Add white lines at the top of each division within the column
        y = (num_divisions - 1) + 0.5 - 0.02  # the lines have linewidth=3, so to center the line we need to rest 0.01
        # TODO: need to calculate -0.1 in function of the dimensions of the case, 0.1 is = -0.1 + 0.2
        #  (extension of the line)
        x1, y1 = [-0.07, 0.07], [y, y]
        inc_x = [column_width+column_distance, column_width+column_distance]
        for i in range(num_divisions):
            plt.plot(x1, y1, color="white", linewidth=4)
            x1, y1 = [x1[i] + inc_x[i] for i in range(len(x1))], [y, y]

        # Add the division's lines for each column
        for i in range(7):
            ax.axhline(i, color='grey', lw=1)

        # Add the bar for each of the column based on the data received
        # TODO: Provide the data and escale between 0, 5.5
        result_column_width = column_width / 2
        bar_spacing = result_column_width / 2 
        initial_position = column_width + column_distance
        position = [0] + [initial_position * i for i in range(1, num_divisions)]

        y = list()
        temp_y = self.data.FMMClassification_data_compliance_level
        for i in ['Findable', 'Accessible', 'Interoperable', 'Reusable']:
            # The bar char start with min=0.5 and max=5.5, so we need to add 0.5 to the values
            y.append(temp_y[i]+0.5)
        
        if self.overlay_plots:
            y2 = list()
            temp_y2 = self.data2.FMMClassification_data_compliance_level
            for i in ['Findable', 'Accessible', 'Interoperable', 'Reusable']:
            # The bar char start with min=0.5 and max=5.5, so we need to add 0.5 to the values
                y2.append(temp_y2[i]+0.5)

        # y = [0.5, 1.5, 3.5, 0.48]
        for i in range(4):
            if self.overlay_plots:
                if i == 0:
                    ax.bar(position[i]-bar_spacing, y2[i], bottom=0, alpha=0.6, color=self.color1, edgecolor='none', width=result_column_width, label=self.data_name)
                    ax.bar(position[i]+bar_spacing, y[i], bottom=0, alpha=0.6, color=self.color2, edgecolor='none', width=result_column_width, label=self.data2_name)
                else:
                    ax.bar(position[i]-bar_spacing, y2[i], bottom=0, alpha=0.6, color=self.color1, edgecolor='none', width=result_column_width)
                    ax.bar(position[i]+bar_spacing, y[i], bottom=0, alpha=0.6, color=self.color2, edgecolor='none', width=result_column_width)
            else:
                ax.bar(position[i], y[i], bottom=0, alpha=0.6, color=self.color1, edgecolor='none', width=result_column_width)
            col_name = list({j for j in temp_y if temp_y[j] + 0.5 == y[i]})[0]
            ax.text(x=position[i], y=-0.5, s=col_name, horizontalalignment='center', fontsize=18,
                    color=self.cmap(color_value), weight='semibold')
            
            

        # Hide the x-axis and y-axis
        ax.axis('off')

        # Set the limits for the x-axis and y-axis
        ax.set_xlim([-1.25, (column_width + column_distance) * 4 - column_distance + column_width])
        ax.set_ylim([-0.5, num_divisions + 1])

        ax.set_title(label='FDM FAIRness Level score'+(f"\n{self.data_name} vs {self.data2_name}" if self.overlay_plots else ""), fontsize=24, color=self.cmap(1.0), weight='semibold')
        
        if self.overlay_plots:
            ax.legend(loc="center right",
                    bbox_to_anchor=(0.62, 0.15, 0.5, 0.5),
                    fontsize=20)
            
        plt.tight_layout(rect=[0, 0, 1, 0.94])

        
        
    def pie_chart(self, data, data_name=""):
        def func(pct, allvals):
            absolute = int(np.round(pct / 100. * np.sum(allvals)))
            return f"{absolute:d}\n({pct:.1f}%)"

        # Data for the pie chart
        labels = list(data.FMMClassification_data_length.keys())
        sizes = [data.FMMClassification_data_length[x] for x in labels]

        # Create the figure and axes
        fig, ax = plt.subplots(figsize=(15, 10))

        # Define colors for the wedges
        colors = [self.cmap(i / max(len(labels), 1)) for i in range(len(labels)+1)][-3:][::-1]
        
        # Generate the pie chart
        wedges, texts, autotexts = ax.pie(sizes,
                                          colors=colors,
                                          autopct=lambda pct: func(pct, sizes),
                                          startangle=90,
                                          textprops=dict(weight="bold", color="white", size=20))

        # Apply path effects (stroke) to label text
        for text in texts + autotexts:
            text.set_path_effects([
                path_effects.Stroke(linewidth=2, foreground='black'),  # Outline
                path_effects.Normal()  # Original text
            ])
        
        # Add a title
        ax.set_title(label=f'Distribution of priorities'+(f"\n for {data_name}" if self.overlay_plots else ""), fontsize=24, color=self.cmap(1.0), weight='semibold')

        # legend
        ax.legend(wedges, labels,
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1),
                  fontsize=20,)

        # Hide the x-axis and y-axis
        ax.axis('off')
        
        plt.tight_layout(rect=[0, 0, 1, 0.94])

    def cumulative_proportion_bar_chart(self):
        """
        Generate a cumulative proportion bar chart comparing one or two datasets.

        This method visualizes the proportion of different categories (defined by `FMMClassification_data_length`)
        as stacked bar segments, where each segment's height represents its relative proportion of the total.
        
        If `overlay_plots` is True, it displays two bars side-by-side (one for each dataset) for comparison.
        Each segment is labeled with both the count and the percentage it represents.

        Assumes that the instance has the following attributes:
            - self.data: Object with attribute `FMMClassification_data_length` (dict of category counts).
            - self.data2: (Optional) Secondary object with the same structure, used for overlay.
            - self.overlay_plots: Boolean indicating whether to compare two datasets.
            - self.color1, self.color2: Colors used to distinguish between datasets.
            - self.data_name, self.data2_name: Names shown on the bars for each dataset.
            - self.cmap: Colormap used to generate segment colors.

        Produces:
            - A matplotlib figure with one or two stacked bars.
            - Each segment of the bar shows its raw count and percentage of the total.
            - A legend is shown for category labels.
        """
        
        labels = list(self.data.FMMClassification_data_length.keys())
        sizes1 = np.array([self.data.FMMClassification_data_length[x] for x in labels], dtype=float)
        total1 = sizes1.sum()
        props1 = sizes1 / total1  # proportions sum to 1

        if self.overlay_plots:
            sizes2 = np.array([self.data2.FMMClassification_data_length.get(x, 0) for x in labels], dtype=float)
            total2 = sizes2.sum()
            props2 = sizes2 / total2
        else:
            sizes2 = None
            props2 = None

        fig, ax = plt.subplots(figsize=(15, 10))

        bar_width = 0.4
        x = np.arange(len(labels))

        colors = [self.cmap(i / max(len(labels), 1)) for i in range(len(labels)+1)][-3:][::-1]

        def draw_bar(x_pos, props, sizes, label, color):
            bottom = 0
            for i, (prop, count) in enumerate(zip(props, sizes)):
                if prop == 0:
                    continue  # skip zero-size segments
                ax.bar(x_pos, prop, bar_width, bottom=bottom, color=colors[i], edgecolor=colors[i])

                # Add label inside each segment
                y_center = bottom + prop / 2
                percent_str = f"{int(count)} ({prop*100:.1f}%)"
                ax.text(x_pos, y_center, percent_str,
                        ha='center', va='center', fontsize=14, weight='bold', color='black' if i != 0 else "white")
                bottom += prop

            # Add label at top
            ax.text(x_pos, 1.03, label, ha='center', fontsize=18, weight='bold', color=color)

        if self.overlay_plots:
            draw_bar(x[0] - bar_width, props1, sizes1, self.data_name or "Data 1", self.color1)
            draw_bar(x[0] + bar_width, props2, sizes2, self.data2_name or "Data 2", self.color2)

            ax.set_xlim(x[0] - 1, x[0] + 1)
        else:
            draw_bar(0, props1, sizes1, self.data_name or "", self.color1)
            ax.set_xlim(-1, 1)

        # Add legend
        handles = [plt.Rectangle((0, 0), 1, 1, color=colors[i]) for i in range(len(labels))]
        ax.legend(handles, labels, fontsize=16, title="Categories")

        ax.set_ylim(0, 1.1)
        ax.set_ylabel("Proportion", fontsize=20, weight='bold')
        ax.set_xticks([])
        ax.yaxis.grid(True, linestyle='--', alpha=0.7)

        # Title
        ax.set_title(f'Distribution of Priorities' + (f"\n for {self.data_name} and {self.data2_name}" if self.overlay_plots else ""),
                    fontsize=24, color=self.cmap(1.0), weight='semibold')

        plt.tight_layout(rect=[0, 0, 1, 0.94])
