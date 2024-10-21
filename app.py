import pandas as pd
import plotly.express as px
import panel as pn

# Enable Panel extensions
pn.extension('plotly', 'tabulator')

# Load the dataset
data = pd.read_csv('covid_data.csv')

# Define the template with improved layout
template = pn.template.FastGridTemplate(
    title="COVID-19 Dashboard",
    accent_base_color="#BB2649",  # Custom theme colors
    header_background="#BB2649",
    theme='dark',
    row_height=150
)

# Filter Widgets with standard names
country_filter = pn.widgets.Select(
    name='Select Country', options=[None] + list(data['Country/Region'].unique()), width=300
)
region_filter = pn.widgets.Select(
    name='WHO Region', options=[None] + list(data['WHO Region'].unique()), width=300, disabled=True
)

# Arrange filters in a row
filters_row = pn.Row(
    country_filter,
    region_filter,
    sizing_mode='fixed',
    align='center',
    margin=(0, 0, 10, 0)
)

# Define card colors with subtle shades
color_confirmed = '#FFA07A'  # Light Salmon
color_deaths = '#FFB6C1'     # Light Pink
color_recovered = '#98FB98'  # Pale Green

# Define cards with updated titles and lighter colors
card_confirmed = pn.pane.HTML(f"""
    <div style="background-color: black; padding: 10px; border-radius: 5px; text-align: center; color: white; height: 100%; display: flex; flex-direction: column; justify-content: center;">
        <h4 style="font-weight: bold; font-size: 20px; color: {color_confirmed}; margin: 0;">Total Confirmed Cases:</h4>
        <p id="confirmed-value" style="font-weight: bold; font-size: 28px; color: {color_confirmed}; margin: 10px 0 0 0;">N/A</p>
    </div>
""", width=200, height=100, sizing_mode='stretch_both')

card_deaths = pn.pane.HTML(f"""
    <div style="background-color: black; padding: 10px; border-radius: 5px; text-align: center; color: white; height: 100%; display: flex; flex-direction: column; justify-content: center;">
        <h4 style="font-weight: bold; font-size: 20px; color: {color_deaths}; margin: 0;">Total Deaths:</h4>
        <p id="deaths-value" style="font-weight: bold; font-size: 28px; color: {color_deaths}; margin: 10px 0 0 0;">N/A</p>
    </div>
""", width=200, height=100, sizing_mode='stretch_both')

card_recovered = pn.pane.HTML(f"""
    <div style="background-color: black; padding: 10px; border-radius: 5px; text-align: center; color: white; height: 100%; display: flex; flex-direction: column; justify-content: center;">
        <h4 style="font-weight: bold; font-size: 20px; color: {color_recovered}; margin: 0;">Total Recovered:</h4>
        <p id="recovered-value" style="font-weight: bold; font-size: 28px; color: {color_recovered}; margin: 10px 0 0 0;">N/A</p>
    </div>
""", width=200, height=100, sizing_mode='stretch_both')

# Combine filters and cards in one section
filters_and_cards = pn.Column(
    filters_row,
    pn.Row(
        card_confirmed,
        card_deaths,
        card_recovered,
        sizing_mode='stretch_both',
        align='center',
        margin=(20, 0)
    ),
    sizing_mode='stretch_both'
)

# Define color palettes for pie and bar charts
pie_chart_colors = ['#FFA07A', '#98FB98', '#ADD8E6', '#FFDEAD', '#DDA0DD', '#B0E0E6']
bar_chart_colors = ['#87CEFA', '#9370DB', '#FFC0CB', '#90EE90', '#AFEEEE', '#FFB6C1']

# Define Chart Functions with subtle colors
def create_pie_chart(column):
    df = data.groupby('WHO Region')[column].sum().reset_index()
    fig = px.pie(df, names='WHO Region', values=column, title=f'{column} Distribution by WHO Region')
    fig.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font_color='white',
        title_font_color='white',
        legend_title_font_color='white',
        legend_font_color='white'
    )
    fig.update_traces(marker=dict(colors=pie_chart_colors))  # Applying the subtle color palette to the pie chart
    return pn.pane.Plotly(fig, height=400, width=500, sizing_mode='stretch_both')

def create_bar_chart():
    df = data.groupby('WHO Region')['Recovered'].sum().reset_index()
    fig = px.bar(df, x='WHO Region', y='Recovered', title='Recovered Cases by WHO Region')
    fig.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font_color='white',
        title_font_color='white',
        xaxis_title_font_color='white',
        yaxis_title_font_color='white'
    )
    fig.update_traces(marker_color=bar_chart_colors)  # Applying the subtle color palette to the bar chart
    return pn.pane.Plotly(fig, height=400, width=500, sizing_mode='stretch_both')

def update_data(event):
    country = country_filter.value
    if country:
        filtered_data = data[data['Country/Region'] == country]
        region = filtered_data['WHO Region'].iloc[0] if not filtered_data.empty else 'N/A'
        
        total_confirmed = filtered_data['Confirmed'].sum() if not filtered_data.empty else 'N/A'
        total_deaths = filtered_data['Deaths'].sum() if not filtered_data.empty else 'N/A'
        total_recovered = filtered_data['Recovered'].sum() if not filtered_data.empty else 'N/A'
        
        card_confirmed.object = f"""
            <div style="background-color: black; padding: 10px; border-radius: 5px; text-align: center; color: white; height: 100%; display: flex; flex-direction: column; justify-content: center;">
                <h4 style="font-weight: bold; font-size: 20px; color: {color_confirmed}; margin: 0;">Total Confirmed Cases:</h4>
                <p style="font-weight: bold; font-size: 28px; color: {color_confirmed}; margin: 10px 0 0 0;">{total_confirmed:,.0f}</p>
            </div>
        """
        card_deaths.object = f"""
            <div style="background-color: black; padding: 10px; border-radius: 5px; text-align: center; color: white; height: 100%; display: flex; flex-direction: column; justify-content: center;">
                <h4 style="font-weight: bold; font-size: 20px; color: {color_deaths}; margin: 0;">Total Deaths:</h4>
                <p style="font-weight: bold; font-size: 28px; color: {color_deaths}; margin: 10px 0 0 0;">{total_deaths:,.0f}</p>
            </div>
        """
        card_recovered.object = f"""
            <div style="background-color: black; padding: 10px; border-radius: 5px; text-align: center; color: white; height: 100%; display: flex; flex-direction: column; justify-content: center;">
                <h4 style="font-weight: bold; font-size: 20px; color: {color_recovered}; margin: 0;">Total Recovered:</h4>
                <p style="font-weight: bold; font-size: 28px; color: {color_recovered}; margin: 10px 0 0 0;">{total_recovered:,.0f}</p>
            </div>
        """
        
        # Update the WHO Region filter value
        region_filter.value = region
        
        # Update the charts
        bar_chart.object = create_bar_chart()
        pie_chart_cases.object = create_pie_chart('Confirmed')
        pie_chart_deaths.object = create_pie_chart('Deaths')
    else:
        # Reset data when no country is selected
        card_confirmed.object = f"""
            <div style="background-color: black; padding: 10px; border-radius: 5px; text-align: center; color: white; height: 100%; display: flex; flex-direction: column; justify-content: center;">
                <h4 style="font-weight: bold; font-size: 20px; color: {color_confirmed}; margin: 0;">Total Confirmed Cases:</h4>
                <p style="font-weight: bold; font-size: 28px; color: {color_confirmed}; margin: 10px 0 0 0;">N/A</p>
            </div>
        """
        card_deaths.object = f"""
            <div style="background-color: black; padding: 10px; border-radius: 5px; text-align: center; color: white; height: 100%; display: flex; flex-direction: column; justify-content: center;">
                <h4 style="font-weight: bold; font-size: 20px; color: {color_deaths}; margin: 0;">Total Deaths:</h4>
                <p style="font-weight: bold; font-size: 28px; color: {color_deaths}; margin: 10px 0 0 0;">N/A</p>
            </div>
        """
        card_recovered.object = f"""
            <div style="background-color: black; padding: 10px; border-radius: 5px; text-align: center; color: white; height: 100%; display: flex; flex-direction: column; justify-content: center;">
                <h4 style="font-weight: bold; font-size: 20px; color: {color_recovered}; margin: 0;">Total Recovered:</h4>
                <p style="font-weight: bold; font-size: 28px; color: {color_recovered}; margin: 10px 0 0 0;">N/A</p>
            </div>
        """
        
        # Clear the WHO Region filter value
        region_filter.value = ''
        
        # Clear the charts
        bar_chart.object = create_bar_chart()
        pie_chart_cases.object = create_pie_chart('Confirmed')
        pie_chart_deaths.object = create_pie_chart('Deaths')

# Create components
bar_chart = pn.panel(create_bar_chart())
pie_chart_cases = create_pie_chart('Confirmed')
pie_chart_deaths = create_pie_chart('Deaths')

# Layout arrangement
template.main[0:2, :] = filters_and_cards  # Filters and cards in one section, adjusted height
template.main[2:6, 0:6] = bar_chart  # Bar chart occupies the left side
template.main[2:6, 6:12] = pn.Column(pie_chart_cases, pie_chart_deaths)  # Pie charts stacked vertically on the right

# Bind the country filter to update the data automatically
country_filter.param.watch(update_data, 'value')

# Serve the application
if pn.state.served:
    template.servable()

