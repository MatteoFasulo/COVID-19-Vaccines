loadPackages <- function(libraries){
  if(!"pacman"%in%installed.packages()[,"Package"]){
    install.packages("pacman")
  }
  for (i in 1:length(libraries)){
    pacman::p_load(char=libraries[i])
  }
}
