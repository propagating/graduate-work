#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(tidyverse)
library(reshape2)
library(chron)
library(lubridate)
load("HW5-Data.RData")

meditation = medtn
meditation$program_title = as.factor(meditation$program_title)
meditation$session_type = as.factor(meditation$session_type)
meditation$completed = as.factor(meditation$completed)
meditation$date = as.Date(meditation$date)
meditation$startTime = hour(meditation$logged_at_local) + minute(meditation$logged_at_local)/60
meditation$durationMin = meditation$duration_in_sec/60
onlyCompleted = meditation %>% filter(as.integer(completed) == 2)

axisFormatting = element_text(size = 20)
tickFormatting = element_text(size = 14)

#working w a dataset from BC
ui = fluidPage(
    titlePanel("Meditation Data", windowTitle = "Meditation Data"),
    sidebarLayout(
        sidebarPanel(
            selectInput("participantId","Participant ID",choices=meditation$ID, selected=0),
            uiOutput("dateSelect"),
            radioButtons("showCompleted","Show Completed Sessions Only?",c("Yes","No"), selected ="No")
        ),
        mainPanel(textOutput("nrow"),
                  br(),
                  plotOutput("meditationPlot", click = "plot_click",
                             dblclick = "plot_dblclick",
                             hover = "plot_hover",
                             brush = "plot_brush"),
                  br(),

                  htmlOutput("plotInformation"),
                  br(),
                  br(),
                  HTML("<h3>Surprising Data Metrics</h3>"),
                  br(),
                  HTML("<p>I was surprised at how few incomplete sessions there were across the entire data set. Initially, I expected to find a pretty significant difference when</br>
                       graphing complete vs incomplete sessions, but for the most part, the graphed changes were not noticable, and the effects of the mean were minimal.
                       <br/> This can be verified by selecting a similar range on the graph toggling between the options of 'Show Completed Sessions Only'.<br/>
                       </p>"),
                  br(),
                  br(),
                  HTML("<h3>Interesting Applications of RShiny</h3>"),
                  br(),
                  HTML("<p>The most interseting bit I discovered while creating this sample application is how RShiny creates event handlers through an onbservable input.</br>
                       While power, they do not necessarily play nice when updating existing UI elements in large or complex operations.
                       <br/> As a result it's typically better to add in a render function for the ui element that you intend to update within your event handler. <br/>
                       </p>")
        )
    ))
server = function(input,output, session){

    observe({
        x <- input$participantId
        pData = meditation %>% filter(ID == x)
        minDate = meditation %>%
            filter(ID == x) %>%
            filter(date == min(date))
        maxDate = meditation %>%
            filter(ID == x) %>%
            filter(date == max(date))

        output$dateSelect = renderUI({
            dateRangeInput("dateSelect","Date Range",
                           start = min(minDate$date),
                           min= min(minDate$date),
                           end = max(maxDate$date),
                           max = max(maxDate$date))
        })
    })

    observe({
        x <- input$showCompleted
        session$resetBrush("plot_brush")
        output$meditationPlot = renderPlot({

            if(input$showCompleted == "Yes"){
                filteredData = meditation %>%
                    filter(ID == input$participantId) %>%
                    filter(as.numeric(completed) == 2) %>%
                    filter(date >= input$dateSelect[1] & date <= input$dateSelect[2]) %>%
                    arrange(startTime)
            }else{
                filteredData = meditation %>%
                    filter(ID == input$participantId) %>%
                    filter(date >= input$dateSelect[1] & date <= input$dateSelect[2]) %>%
                    arrange(startTime)
            }
            ggplot(filteredData, aes(x = date, y = startTime)) +
                geom_point(size = 3, aes(col = durationMin, shape = session_type)) +
                scale_y_continuous(name="Start Time",
                                   breaks = c(0, 4, 8, 12, 16, 20, 24),
                                   labels = c("12AM", "4AM", "8AM", "12PM", "4PM", "8PM", "12AM")) +
                scale_colour_gradient(low = "yellow",
                                      high = "red") +
                labs(shape = "Activity Type", col="Duration (min)", x = "Date") +
                theme(axis.title = axisFormatting,
                      axis.text = tickFormatting,
                      legend.title = tickFormatting)
        })

        output$plotInformation <- renderText({
            if(input$showCompleted == "Yes"){
                filteredData = meditation %>%
                    filter(ID == input$participantId) %>%
                    filter(as.numeric(completed) == 2) %>%
                    filter(date >= input$dateSelect[1] & date <= input$dateSelect[2]) %>%
                    arrange(startTime)
            }else{
                filteredData = meditation %>%
                    filter(ID == input$participantId) %>%
                    filter(date >= input$dateSelect[1] & date <= input$dateSelect[2]) %>%
                    arrange(startTime)
            }
            totalPoints = brushedPoints(filteredData, input$plot_brush, allRows = FALSE)
            xy_str <- function(e) {
                if(is.null(e)) return("Please click and drag on the graph to select data\n")
                paste0("x=", round(e$x, 1), " y=", round(e$y, 1), "\n")
            }
            xy_range_str <- function(e) {
                if(is.null(e)) return("Please click and drag on the graph to select data\n")
                paste0("xmin=", round(e$xmin, 1), " xmax=", round(e$xmax, 1),
                       " ymin=", round(e$ymin, 1), " ymax=", round(e$ymax, 1))
            }

            if(count(totalPoints) == 0){
                paste0("Please click and drag on the graph to select data.")
            }else{
                paste0("There were ", count(totalPoints)," obersvations selected. The average duration for these observations is ", round(mean(totalPoints$durationMin), digits = 2),".")
            }

        })
    })


}

#can also print(ui) to see raw html, if want
shinyApp(ui=ui,server=server)
