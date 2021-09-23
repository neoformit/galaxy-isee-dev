"""Pre-configured iSEE options for selection by user.

These are preconfigured iSEE parameters that can be chosen by the user
as multiple choice (checkbox/select) input fields. Each parameter
(e.g. "initial") has a list of options whose indices should match the value of
the input field in the tool XML.

In all likelihood, the majority of options in
iSEE don't make sense without first being able to sniff the data and so are not
feasible to expose in the Galaxy tool form. Currently you will see that only
plot type and width can be exposed.

Currently user configuration is NOT IMPLEMENTED - the code is here but option
is hidden from user in the tool form. Without ``custom`` selection, this simply
returns a DEFAULT iSEE configuration (defined at the bottom of this file).
"""


def app(custom):
    """Render R code to create iSEE app from user input."""
    call = "app <- iSEE(sce"

    if custom['selected']:
        # User specified layout in tool form
        if custom['method']['selected'].value == 'choice':
            # Template choices into call
            call = render_plots(call, custom['method']['plots'])

            # Don't think this is feasible:
            # call = render_colormap(call, custom['choice']['colormap'])

            # Do "extras" make sense?
            # call = render_extras(call, custom['choice']['extras'])

        elif custom['custom']['method']['selected'].value == 'custom':
            # Template custom R code - NOT YET CONFIGURED
            pass

    return f"{call})"

    # Default layout selected
    return DEFAULT


def render_plots(call, plots):
    """Render plot calls from user input."""
    if not plots:
        return call
    plot_calls_list = [
        get_render_func(plot)(
            # user plot params as kwargs here
        )
        for plot in plots
    ]
    plot_calls = ',\ninitial=c(\n' + ',\n'.join(plot_calls_list) + ')'
    return call + plot_calls


def get_render_func(plot):
    """Return the appropriate function to render plot."""
    return OPTIONS['plots'][plot['plot_types']['plot_type'].value]


def reduced_dimension_plot(pw="6L"):
    """Render a ReducedDimensionPlot object call."""
    return (
        f'''ReducedDimensionPlot(
        PanelWidth={pw})''')


def feature_assay_plot(pw="6L"):
    """Render a FeatureAssayPlot object call."""
    return (
        f'''FeatureAssayPlot(
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


DEFAULT = """
# NB: This option is depricated - Looks like the new way is to set configs in
#     the sce itself - which can happen outside iSEE.
#     Should it be omitted?
sce <- registerAppOptions(sce, color.maxlevels=40)


categorical_color_fun <- function(n){
  if (n <= 37) {
    # Less than 37 colours, use something from colour brewer
    # (joining a bunch of palettes, best colours up front)
    multiset <-  c(
        RColorBrewer::brewer.pal(9, "Set1"),
        RColorBrewer::brewer.pal(8, "Set2"),
        RColorBrewer::brewer.pal(12, "Set3"),
        RColorBrewer::brewer.pal(8, "Dark2"))
    return(multiset[1:n])
  }
  else {
    # More that 37, well at least it looks pretty
    return(rainbow(n))
  }
}


ecm <- ExperimentColorMap(

  # The default is viridis::viridis
  # https://cran.r-project.org/web/packages/viridis/vignettes/intro-to-viridis.html#the-color-scales
  # Setting continous is entirely a matter of taste
  # Some find magma easier to read than viridis

  all_continuous = list(
    assays  = viridis::magma,
    colData = viridis::magma,
    rowData = viridis::magma
  ),
  all_discrete = list(
    colData = categorical_color_fun,
    rowData = categorical_color_fun
  )
)


# These options are all sce-contents agnostic.
initial_plots <- c(

  # Show umap with clusters by default
  ReducedDimensionPlot(
                   DataBoxOpen=TRUE,
                   ColorBy="Column data",
                   VisualBoxOpen=TRUE,
                   PanelWidth=6L),

  # Show gene expression plot separated (and coloured) by cluster, by default.
  FeatureAssayPlot(XAxis = "Column data",
                   DataBoxOpen=TRUE,
                   VisualBoxOpen=TRUE,
                   ColorBy="Column data",
                   PanelWidth=6L
                   ),
  # Gene list is better wide
  RowDataTable(PanelWidth=12L),

  # For cell level observations (QC.)
  ColumnDataPlot(PanelWidth=6L,
                 DataBoxOpen=TRUE,
                 VisualBoxOpen=TRUE )
)

app <- iSEE(sce,
            colormap=ecm,
            initial=initial_plots)
"""
