# Daniel Moscoe

# Question 2. Often you are asked whether particular states are improving their mortality rates (per cause) faster than, or slower than, the national average. Create a visualization that lets your clients see this for themselves for one cause of death at a time. Keep in mind that the national average should be weighted by the national population.

#https://dmoscoe.shinyapps.io/hw3q2_2109301241/

library(shiny)
library(tidyverse)

df <- read_csv("https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv")

ui <- fluidPage(
    headerPanel("National and State Mortality by Cause, 1999-2010"),
    sidebarPanel(
        selectInput("icd", "Cause of death", sort(unique(df$ICD.Chapter))),
        selectInput("st", "State", sort(unique(df$State)))
    ),
    mainPanel(
        plotOutput("plt"),
        HTML(r"(Data available at <A HREF = "https://wonder.cdc.gov/ucd-icd10.html">CDC WONDER</A>.)")
    )
)

server <- shinyServer(function(input, output, session) {
    filtered_for_icd <- reactive({
        filter(df, ICD.Chapter == input$icd)
    })
    
    national_rates <- reactive({
        filtered_for_icd() %>%
            group_by(Year) %>%
            summarise("United States" = sum(Crude.Rate * Population)/sum(Population))
    })
    
    state_rates <- reactive({
        filtered_for_icd() %>%
            filter(State == input$st) %>%
            rename("State " = Crude.Rate) %>%
            select(Year, "State ")
    })

    to_plot <- reactive({
        full_join(national_rates(), state_rates(), by = "Year") %>%
            pivot_longer(cols = c("United States", "State "), names_to = "Region", values_to = "vals")
    })
    
    output$plt <- renderPlot({
        ggplot(to_plot(), aes(x = Year, y = vals, color = Region)) +
            geom_line(size = 1) +
            xlab("Year") +
            ylab("Deaths per 100k")
    })
})

shinyApp(ui = ui, server = server)