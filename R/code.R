source("https://raw.githubusercontent.com/MatteoFasulo/COVID-19-Vaccines/main/R/util/coreFunctions.R")
loadPackages(libraries=c("dplyr","magrittr","plotly","ggplot2","jsonlite","gamlss","stargazer"))
################################################################################
getLatestVaccubeReport <- function(fileName='data/latest.csv'){
  if (dir.exists('data') == FALSE){
    dir.create('data')
  }
  download.file("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv",fileName)
  vaccines <- read.csv(fileName,encoding = 'UTF-8')
  return(vaccines)
}
vaccines <- getLatestVaccubeReport()

vaccines %>%
  dplyr::select(prima_dose,fornitore) %>%
  group_by(fornitore) %>%
  summarise(prima_dose = sum(prima_dose)) %>%
  as.data.frame(.) %>%
  plot_ly(., labels = ~fornitore, values = ~prima_dose, type = 'pie') %>%
  layout(title = 'Percentage of first doses by manufacturer',
         xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
         yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))

vaccinati <- vaccines[,-c(3,5,6,7,9,10,11,12)]
vaccinati <- vaccinati[which(vaccinati$seconda_dose>0),]
vaccinati$nome_area <- ifelse(vaccinati$nome_area=='Provincia Autonoma Trento','Provincia Autonoma Bolzano / Bozen',vaccinati$nome_area)
vaccinati$nome_area <- ifelse(vaccinati$nome_area=='Provincia Autonoma Bolzano / Bozen','Trentino Alto Adige',vaccinati$nome_area)

vaccinati %>%
  dplyr::select(seconda_dose,fornitore) %>%
  group_by(fornitore) %>%
  summarise(seconda_dose = sum(seconda_dose)) %>%
  as.data.frame(.) %>%
  plot_ly(., labels = ~fornitore, values = ~seconda_dose, type = 'pie') %>%
  layout(title = 'Percentage of second doses by manufacturer',
         xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
         yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))

vaccinati %>%
  dplyr::select(seconda_dose,fornitore,nome_area) %>%
  group_by(nome_area,fornitore) %>%
  summarise(seconda_dose = sum(seconda_dose)) %>%
  as.data.frame(.) %>%
  plot_ly(., x = ~nome_area, y = ~seconda_dose, color = ~fornitore, type = 'bar') %>%
  layout(title = 'Vaccine manufacturer by region',
    xaxis = list(title = "Regione"),
    yaxis = list(title = ""))

vaccinati %>%
  dplyr::select(seconda_dose,fornitore,fascia_anagrafica) %>%
  group_by(fascia_anagrafica,fornitore) %>%
  summarise(seconda_dose = sum(seconda_dose)) %>%
  as.data.frame(.) %>%
  plot_ly(., x = ~fascia_anagrafica, y = ~seconda_dose, color = ~fornitore, type = 'bar') %>%
  layout(title = 'Vaccine manufacturer by age-group',
         xaxis = list(title = "Fascia di età"),
         yaxis = list(title = ""))

vaccinati %>%
  dplyr::select(nome_area,seconda_dose,fornitore,fascia_anagrafica) %>%
  group_by(nome_area,fascia_anagrafica,fornitore) %>%
  summarise(seconda_dose = sum(seconda_dose)) %>%
  as.data.frame(.) %>%
  ggplot(., aes(x = fascia_anagrafica, y = seconda_dose, fill = fornitore)) +
  geom_bar(stat = 'identity', position = 'stack') + facet_grid(rows = vars(nome_area), scales = "free", space = "free") +
  coord_flip() +
  theme(strip.text.y = element_text(angle = 0, size=rel(2)),
        axis.text.y = element_text(angle = 0, size=rel(2))) +
  ylab("")+
  xlab("Fascia di età")

ggsave('complete.png',dpi = 320, height = 28, width = 16)


getDataFromJSON <- function(fileName='regionSVI_PIL.json'){
  temp <- fromJSON(fileName,flatten = T)
  indexSVI <- as.data.frame(do.call(rbind, temp))
  indexSVI$codice_regione_ISTAT <- row.names(indexSVI)
  return(indexSVI)
}
indexSVI <- getDataFromJSON()


finalDF <- merge(vaccinati,indexSVI,by="codice_regione_ISTAT")
finalDF$coverage <- NA
finalDF %<>%
  mutate(coverage = round(as.numeric(tot_Dosi)/as.numeric(residenti),3),
         PIL = as.numeric(PIL),
         mono_Family = as.numeric(mono_Family),
         six_more_Family = as.numeric(six_more_Family),
         low_Educ = as.numeric(low_Educ),
         house_Crow = as.numeric(house_Crow),
         ass_Unease = as.numeric(ass_Unease),
         u30_Unemployed = as.numeric(u30_Unemployed),
         eco_Unease = as.numeric(eco_Unease))

model <- lm(coverage~PIL+mono_Family+six_more_Family+low_Educ+house_Crow+ass_Unease+u30_Unemployed+eco_Unease, data=finalDF)
step.model <- step(model, direction = "backward",trace = F,k=log(nrow(finalDF)))
summary(step.model)

stargazer(cbind(Coef = coef(step.model), confint(step.model)), summary = F)

finalDF$binCoverage <- cut(finalDF$coverage,breaks = c(0,mean(finalDF$coverage),0.85), labels = c(0,1))
logit.model <- gamlss(binCoverage~PIL+mono_Family+six_more_Family+low_Educ+house_Crow+ass_Unease+u30_Unemployed+eco_Unease,family=BI(),data=finalDF)
summary(logit.model)

logisticOutput <- exp(cbind(OR = coef(logit.model), confint(logit.model)))
logisticOutput <- as.data.frame(logisticOutput)
stargazer(logisticOutput, summary = F)
