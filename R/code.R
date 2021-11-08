source("https://raw.githubusercontent.com/MatteoFasulo/Rare-Earth/main/util/coreFunctions.R")
loadPackages(libraries=c("stargazer","plm"))
################################################################################


descrStats <- stargazer(type="text", summary = T, title = "Descriptive statistics.", align = T, )

CDTest <- pcdtest(x, test = c("cd","lm"))
