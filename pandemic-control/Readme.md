# Readme

This folder contains the scripts and data needed for reproducing the lower panels in figure 2 as well as figure 4 in the main text. It also includes the script and data needed for reproducing figures S10 and S11 in the Supplementary.

The data is generated using a slighlty modified version of the model code found here: https://zenodo.org/record/3727255#.YCPhm89Kj7g for the growth rate of COVID-post intervention (isolation+contact tracing). The code solves the integral operator version of the Euler-Lotka equation (Ferretti, Wymant et al, Science 2020) The original code solves the equation for a case isolation and quarantine efficacy values from 0 to 100%, and outputs a matrix of r values. The modified code sets a fixed value for isolation efficacy and reads a matrix of quarantine efficacies from a file (eff.txt). The output is a matrix of r values, as for the original model.

The modification is in GeneralisedEulerLotka_solution_rate_uptake.R
