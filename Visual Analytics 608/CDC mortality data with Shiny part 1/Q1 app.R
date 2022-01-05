#Daniel Moscoe

#Question 1. As a researcher, you frequently compare mortality rates from particular causes across different states. You need a visualization that will let you see (for 2010 only) the crude mortality rate, across all states, from one cause (for example, neoplasms...). Create a visualization that allows you to rank states by crude mortality for each cause of death.

#https://dmoscoe.shinyapps.io/hw3q1_2109301137/

library(shiny)
library(tidyverse)

df <- read_csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv") %>%
    filter(Year == 2010)

ui <- fluidPage(
    headerPanel("Deaths per 100k by state, 2010"),
    sidebarPanel(
        selectInput("icd", "Cause of death", sort(unique(df$ICD.Chapter)))
    ),
    mainPanel(
        plotOutput("plt", height = "800px"),
        ("Solid vertical line indicates national average.")
    )
)

server <- shinyServer(function(input, output, session){
    filtered_for_icd <- reactive({
        filter(df, ICD.Chapter == input$icd)
    })
    
    national_rate <- reactive({
        filtered_for_icd() %>%
            mutate("prod" = Crude.Rate * Population) %>%
            summarise(sum(prod)/sum(Population)) %>%
            as.numeric()
    })
    
    output$plt <- renderPlot({
        ggplot(filtered_for_icd(), aes(x = Crude.Rate, y = reorder(State, Crude.Rate))) + 
            geom_point() +
            geom_vline(xintercept = national_rate()) +
            xlab("Deaths per 100k") +
            ylab("")
    })
    
})

shinyApp(ui = ui, server = server)



