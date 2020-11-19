library(tidyverse)
library(reshape2)
library(scales)
library(shiny)
library(DT)

#ORGANIZING DATASET
crimeData = read.csv('UOF_BY_DEPARTMENTS.csv', head=TRUE)
factorCols <- c("Town_county","pd_dept_plus_county","pd_dept","county","coverage_city")

crimeData[factorCols] <- lapply(crimeData[factorCols], factor)

crimeDataMin = data.frame(
    "WhitePopulation"= crimeData$pctwhite_adjpop, "BlackPopulation"= crimeData$pctblack_adjpop, "HispanicPopulation"= crimeData$pcthisp_adjpop, "AsianPacificPopulation"= crimeData$pctasian_adjpop,
    "WhiteOfficers"= crimeData$white_pct_officers, "BlackOfficers"= crimeData$black_pct_officers, "HispanicOfficers"= crimeData$hispanic_pct_officers, "AsianPacificOfficers"= crimeData$asian_pacific_islander_pct_officers,
    "ComplianceHold"= crimeData$pct_complaince_hold, "HandFists"= crimeData$pct_hands_fists,"PepperSpray"= crimeData$pct_pepper_spray,"Baton"= crimeData$pct_baton, "LegStrike"= crimeData$pct_leg_strikes,
    "TakeDown"= crimeData$pct_take_down,"DeadlyForce"= crimeData$pct_deadly_force)

demo = colnames(crimeDataMin)[1:8]
for (i in demo){
    crimeDataMin = mutate(crimeDataMin, !!paste0(i,"Quantile") := ntile(crimeDataMin[which(colnames(crimeDataMin)==i)],4))
    as.factor(crimeDataMin[which(colnames(crimeDataMin)==paste0(i,"Quantile"))])
}

crimeDataMin <- crimeDataMin[9:23]
crimeDataMin = unnest(crimeDataMin, colnames(crimeDataMin))


head(crimeDataMin)
ui = fluidPage(
    titlePanel("Police Use of Force Across Department & Community Race Profiles", windowTitle = "Group Module 2"),
    sidebarLayout(
        sidebarPanel(
            div("1). Select a target race demographic for the police department and community they serve."),
            br(),
            div("2). Select % of race that makes up the police department and community."),
            br(),
            div("NOTE: If no % value is selected, all police departments or communities will be used."),
            br(),
            selectInput("raceOffInput","Department Race",c("White","Black","Hispanic","AsianPacific")),
                     checkboxGroupInput("quanOffInput","Department Race %",
                                        c("< 25%" = 1, "25% - 50%" = 2, "50% - 75%" = 3,"> 75%" = 4), selected=c(2)),
                     selectInput("racePopInput","Population Race",c("White","Black","Hispanic","AsianPacific")),
                     checkboxGroupInput("quanPopInput","Population Race %", c("< 25%" = 1, "25% - 50%" = 2, "50% - 75%" = 3,"> 75%" = 4), selected=c(2)), width=3),

        mainPanel(plotOutput("plotComparison"),
                  textOutput("filterCount"),
                  ("Red bar indicates average % of all departments."),
                  br(),
                  br(),
                  br(),
                  h3("Does a Significant Difference Exist Between the Filtered and Unfiltered Groups?", width = "100%", align ="center"),
                  br(),
                  div(),
                  br(),
                  dataTableOutput("statTests"),
                  br(),
                  HTML("
                  <div id='statKey'>
    <div><span style=\"display:inline-block; width:15px; height : 15px; margin-right :15px; background-color : rgba(122,13,13,0.6)\"></span>P-Value < 0.01</div>
    <div><span style=\"display:inline-block; width:15px; height : 15px; margin-right :15px; background-color : rgba(209,121,6,0.5)\"></span>P-Value < 0.05</div>
    <div><span style=\"display:inline-block; width:15px; height : 15px; margin-right :15px; background-color : rgba(227,210,30,0.3)\"></span>P-Value < 0.10</div>
    <div><span style=\"display:inline-block; width:15px; height : 15px; margin-right :15px; background-color : rgba(30,227,30,0.1)\"></span>P-Value > 0.1</div>
    <div><span style=\"display:inline-block; width:15px; height : 15px; margin-right :15px; background-color : rgba(120,120,120,0.1)\"></span>P-Value Unavailable</div>
</div>"),
                  div("The table above contains p-values of a t-test conducted between the deparments that meet the filter criteria against: "),
                  div("(1) All Departments, including those in the filter group"),
                  div("(2) All Deparments, excluding the filter group"),
                  br(),
                  br(),
                  br(),
                  h3("What are the Raw Values for Comparison?", width = "100%", align ="center"),
                  br(),
                  DT::dataTableOutput("dataComparison"), width = 9)
    ),
    br(),
    hr(),
    br(),
    div("Riley Kendall and Ryan Richardson", align = "right")

)
server=function(input,output){
    output$plotComparison = renderPlot({

        officerInput = input$quanOffInput
        if (is.null(officerInput) | length(officerInput) == 0) {officerInput=c(1,2,3,4)}
        popInput = input$quanPopInput
        if (is.null(popInput) | length(popInput) == 0) {popInput=c(1,2,3,4)}

        crimeDataFilter <- crimeDataMin %>%
                                filter(get(paste0(input$raceOffInput,"OfficersQuantile")) %in% officerInput &
                                           get(paste0(input$racePopInput,"PopulationQuantile")) %in% popInput)

        output$filterCount = renderText({
            nRows = length(crimeDataFilter$TakeDown)
            nTotal = length(crimeDataMin$TakeDown)
            paste0("The selected filters include ", nRows, " out of ", nTotal," departments.")
        })

        crimeDataOut <- crimeDataMin %>%
            filter(!get(paste0(input$raceOffInput,"OfficersQuantile")) %in% officerInput &
                       !get(paste0(input$racePopInput,"PopulationQuantile")) %in% popInput)

        #AVERAGING, SD, AND COLLECTING FORCE TYPE INFO
        df_forces <- data.frame("ForceTypes" = colnames(crimeDataFilter[1:7]),
                                "overallAverage" = round(as.vector(unlist(lapply(crimeDataMin[1:7], mean))),2),
                                "outsideAverage" =  round(as.vector(unlist(lapply(crimeDataOut[1:7], mean))),2),
                                "filterAverage" = round(as.vector(unlist(lapply(crimeDataFilter[1:7], mean))),2),
                                "overallDeviation" = round(as.vector(unlist(lapply(crimeDataMin[1:7],sd))),2),
                                "outsideDeviaton" =  round(as.vector(unlist(lapply(crimeDataOut[1:7], sd))),2),
                                "filterDeviation" = round(as.vector(unlist(lapply(crimeDataFilter[1:7],sd))),2))

        dt_forces = t(df_forces)
        dt_forces = setNames(data.frame(t(df_forces[,-1])), df_forces[,1])

        row.names(dt_forces) <- c("<b>Average Use % (All Departments)</b>", "<b>Average Use % (Oustide Filter)</b>",
                                  "<b>Average Use % (Inside Filter)</b>", "<b>Std. Dev. % (All Departments)</b>",
                                  "<b>Std. Dev. % (Oustide Filter)</b>", "<b>Std. Dev. % (Inside Filter)</b>")


        tTestFilterComplianceHold <- t.test(crimeDataFilter$ComplianceHold, crimeDataOut$ComplianceHold)
        tTestFilterHandFists <- t.test(crimeDataFilter$HandFists, crimeDataOut$HandFists)
        tTestFilterPepperSpray <- t.test(crimeDataFilter$PepperSpray, crimeDataOut$PepperSpray)
        tTestFilterBaton <- t.test(crimeDataFilter$Baton, crimeDataOut$Baton)
        tTestFilterLegStrike <- t.test(crimeDataFilter$LegStrike, crimeDataOut$LegStrike)
        tTestFilterTakeDown <- t.test(crimeDataFilter$TakeDown, crimeDataOut$TakeDown)
        tTestFilterDeadlyForce <- t.test(crimeDataFilter$DeadlyForce, crimeDataOut$DeadlyForce)
        tTestFilterGroup <- t.test(crimeDataFilter[1:7], crimeDataOut[1:7])

        tTestAllComplianceHold <-t.test(crimeDataFilter$ComplianceHold, crimeDataMin$ComplianceHold)
        tTestAllHandFists <-t.test(crimeDataFilter$HandFists, crimeDataMin$HandFists)
        tTestAllPepperSpray <-t.test(crimeDataFilter$PepperSpray, crimeDataMin$PepperSpray)
        tTestAllBaton <-t.test(crimeDataFilter$Baton, crimeDataMin$Baton)
        tTestAllLegStrike <-t.test(crimeDataFilter$LegStrike, crimeDataMin$LegStrike)
        tTestAllTakeDown <-t.test(crimeDataFilter$TakeDown, crimeDataMin$TakeDown)
        tTestAllDeadlyForce <-t.test(crimeDataFilter$DeadlyForce, crimeDataMin$DeadlyForce)
        tTestOverallGroup <- t.test(crimeDataFilter[1:7], crimeDataOut[1:7])


        forceTypes = unlist(list(colnames(crimeDataFilter[1:7]), "All Force Types"))


        df_tTest = data.frame("ForceTypes" = forceTypes,
                              "T Test (Filter vs Overall)" = round(c(tTestAllComplianceHold$p.value, tTestAllHandFists$p.value,
                                                                     tTestAllPepperSpray$p.value, tTestAllBaton$p.value,
                                                                     tTestAllLegStrike$p.value, tTestAllTakeDown$p.value,
                                                                     tTestAllDeadlyForce$p.value, tTestOverallGroup$p.value),4),
                              "T Test (Filter vs Outside)" =round(c(tTestFilterComplianceHold$p.value, tTestFilterHandFists$p.value,
                                                                    tTestFilterPepperSpray$p.value, tTestFilterBaton$p.value,
                                                                    tTestFilterLegStrike$p.value, tTestFilterTakeDown$p.value,
                                                                    tTestFilterDeadlyForce$p.value, tTestFilterGroup$p.value),4))

        dt_tTest = t(df_tTest)
        dt_tTest = setNames(data.frame(t(df_tTest[,-1])), df_tTest[,1])
        row.names(dt_tTest) <- c("<b>T-Test (Filter vs All)</b>", "<b>T-Test (Filter vs Outside Filter)</b>")
        output$dataComparison = DT::renderDataTable(
            dt_forces,
            selection ='none',
            options = list(searching = FALSE, paging = FALSE, lengthChange=FALSE, info = FALSE), escape = FALSE)

        output$statTests = DT::renderDataTable(
            dt_tTest,
            selection ='none',
            options = list(searching = FALSE, paging = FALSE, lengthChange=FALSE, info = FALSE,
            rowCallback=JS("function(row, data){
	$('td',row).each(function(i){
		if(i == 0) return;
		if(parseFloat(data[i]) == 0){
			$(this).css('background-color','rgba(120,120,120,0.1)');
			$(this).text('NA')
		}
		else if(parseFloat(data[i]) <= 0.01 ){
			$(this).css('background-color','rgba(122,13,13,0.6)');
		}
		else if(parseFloat(data[i]) <= 0.05 ){
			$(this).css('background-color','rgba(209,121,6,0.5)');
		}
		else if(parseFloat(data[i]) <= 0.1){
			$(this).css('background-color','rgba(227,210,30,0.3)');
		}
		else{
			$(this).css('background-color','rgba(30,227,30,0.1)');
		}
	})
}")),escape = FALSE)

        #CREATING PLOT
        ggplot(data = df_forces,aes(x = ForceTypes)) +
            geom_bar(aes(y = filterAverage),
                     stat = "identity",
                     fill = "skyblue",
                     alpha = 0.8) +
            scale_y_continuous(breaks = seq(0, 100, 10),
                               labels = c("0%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"))+
            geom_errorbar(aes(x = ForceTypes,
                              y = filterAverage,
                              ymin = (filterAverage - filterDeviation),
                              ymax = (filterAverage + filterDeviation)),
                          width = 0.2,
                          colour = "orange",
                          alpha = 0.6,
                          size = 1) +
            geom_errorbar(aes(x = ForceTypes,
                              y = overallAverage,
                              ymin = overallAverage,
                              ymax = overallAverage),
                          color = "Red",
                          lty = 2,
                          size = 1) +
            geom_text(aes(y = filterAverage,
                          label = paste0(filterAverage, "%"),
                          vjust = -1.75)) +
            labs(y = "Frequency (%)",
                 x = "Force Used",
                 title = "Frequency of Force Used in Police Interactions") +
            theme(plot.title = element_text(hjust = 0.5, size = 16, face = "bold"))
    })


}
shinyApp(ui=ui,server=server)
