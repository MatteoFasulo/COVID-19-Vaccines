loadPackages <- function(pkgs){
  if(!"pacman"%in%installed.packages()[,"Package"]) install.packages("pacman")
  for (pkg in pkgs){
    pacman::p_load(pkg)
    }
}
