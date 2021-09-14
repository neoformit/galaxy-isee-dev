"""Pre-configured iSEE options for selection by user.

These are preconfigured iSEE parameters that can be chosen by the user
as multiple choice (checkbox/select) input fields. Each parameter
(e.g. "initial") has a list of options whose indices should match the value of
the input field in the tool XML.

For example:

if `params.initial.value = 0`

`PARAM_OPTIONS['initial'][$params.initial[0].value]` should return the
`ReducedDimensionPlot` config.

Thought - this should probably be a set of Python functions to return an R
code block from user params (e.g. plot Type, PanelWidth,  ... ).

"""


def app(custom):
    """Render R code to create iSEE app from user input."""
    call = "app <- iSEE(sce"

    if custom['selected']:
        if custom['method']['selected'].value == 'choice':
            # Template choices into call
            call = render_plots(call, custom['method']['plots'])
            # call = render_colormap(call, custom['choice']['colormap'])
            # call = render_extras(call, custom['choice']['extras'])

        elif custom['custom']['method']['selected'].value == 'custom':
            # Template custom R code
            pass

    return f"{call})"


def render_plots(call, plots):
    """Render plot calls from user input."""
    if not plots:
        return call
    plot_calls = ',\ninitial=c(\n' + ',\n'.join([
        OPTIONS['plots'][plot['plot_types']['plot_type'].value](
             # user plot params here
        )
        for plot in plots
    ]) + ')'
    return call + plot_calls


def reduced_dimension_plot(
        plot_type="UMAP", color_by="Column data",
        color_by_col="cluster", vb_open="FALSE", pw="6L"):
    """Render a ReducedDimensionPlot object call."""
    return (
        f'''ReducedDimensionPlot(
        Type="{plot_type}",
        ColorBy="{color_by}",
        ColorByColumnData="{color_by_col}",
        VisualBoxOpen={vb_open},
        PanelWidth={pw})''')


def feature_assay_plot(
            xaxis="Column data", xaxis_column_data="cluster",
            db_open="FALSE", vb_open="FALSE", color_by="Column data",
            color_by_col="cluster", pw="6L"):
    """Render a FeatureAssayPlot object call."""
    return (
        f'''FeatureAssayPlot(XAxis="{xaxis}",
        XAxisColumnData="{xaxis_column_data}",
        DataBoxOpen={db_open},
        VisualBoxOpen={vb_open},
        ColorBy="{color_by}",
        ColorByColumnData="{color_by_col}",
        PanelWidth={pw})''')


def row_data_table(pw="12L"):
    """Render a RowDataTable object call."""
    return f"RowDataTable(PanelWidth={pw})"


def column_data_plot(pw="6L"):
    """Render a ColumnDataPlot object call."""
    return f"ColumnDataPlot(PanelWidth={pw})"


OPTIONS = {
    'plots': {
        "reduced_dimension_plot": reduced_dimension_plot,
        "feature_assay_plot": feature_assay_plot,
        "row_data_table": row_data_table,
        "column_data_plot": column_data_plot,
    },
    'colormaps': {},
    'extra': {},
}
