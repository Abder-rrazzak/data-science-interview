"""Reproducible Phase 4 demonstrations; data are synthetic."""
import json
import numpy as np
from decision_intelligence.advanced_statistics import (one_way_anova,chi_square_independence,multiple_ols,logistic_regression_demo)

def main():
    rng=np.random.default_rng(42)
    groups={label:rng.normal(mean,5,80) for label,mean in [('A',20),('B',22),('C',25)]}
    x=rng.normal(size=(240,3))
    y=4+1.5*x[:,0]-2*x[:,1]+rng.normal(scale=1.2,size=len(x))
    logits=.7*x[:,0]-.9*x[:,1]
    classes=rng.binomial(1,1/(1+np.exp(-logits)))
    results={'anova':one_way_anova(groups),'chi_square':chi_square_independence([[45,20],[30,50]]),
             'ols':multiple_ols(x,y,['exposure','duration','baseline']),
             'logistic':logistic_regression_demo(x,classes)}
    results['ols'].pop('residuals');results['ols'].pop('fitted')
    print(json.dumps(results,indent=2,allow_nan=False))

if __name__=='__main__':main()
