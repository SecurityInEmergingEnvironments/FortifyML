# Customized NLP score 02
from Interfaces import CustomizedMetricScoreInterface
class CNS02_Accuracy(CustomizedMetricScoreInterface):
  def __init__(self, kwargs):
    CustomizedMetricScoreInterface.__init__(self, kwargs=kwargs)
    self.alpha = self.kwargs['alpha']  # time tradeoff coefficient
    self.beta = self.kwargs['beta']    # natural tradeoff coefficient
    self.gamma = self.kwargs['gamma']  # robust coefficient
    self.showDetails = self.kwargs['showDetails']

  """
  This public method returns the score of the given user-defined metric
  @param scoreDictionary data passed from the user's input data
  @return a dictionary containing the score
  """
  def getScore(self, scoreDictionary):

    naturalaccuracyWithoutDefense = scoreDictionary['baseline_performance']['natural_accuracy']
    robustaccuracyWithoutDefense = scoreDictionary['attacker_performance']['robust_accuracy']

    naturalaccuracyWithDefense = scoreDictionary['defender_performance']['natural_accuracy']
    robustaccuracyWithDefense = scoreDictionary['defender_performance']['robust_accuracy']

    naturalF1ScoreWithoutDefense = scoreDictionary['baseline_performance']['natural_f1-score']
    robustF1ScoreWithoutDefense = scoreDictionary['attacker_performance']['robust_f1-score']

    naturalF1ScoreWithDefense = scoreDictionary['defender_performance']['natural_f1-score']
    robustF1ScoreWithDefense = scoreDictionary['defender_performance']['robust_f1-score']

    naturalaccuracyTradeOff = self.beta * ((naturalaccuracyWithDefense - naturalaccuracyWithoutDefense) / naturalaccuracyWithoutDefense)
    robustaccuracyImprove = self.gamma * ((robustaccuracyWithDefense - robustaccuracyWithoutDefense) / robustaccuracyWithoutDefense)

    naturalF1ScoreTradeOff = self.beta * ((naturalF1ScoreWithDefense - naturalF1ScoreWithoutDefense) / naturalF1ScoreWithoutDefense)
    robustF1ScoreImprove = self.gamma * ((robustF1ScoreWithDefense - robustF1ScoreWithoutDefense) / robustF1ScoreWithoutDefense)

    CNS02_score = (naturalaccuracyTradeOff + robustaccuracyImprove + naturalF1ScoreTradeOff + robustF1ScoreImprove)

    result = {
      "denoiser_name": scoreDictionary['nameOfDefender'],
      "score": CNS02_score,        # required from users
      "details": {
        "weighted_natural_accuracy_tradeOff": naturalaccuracyTradeOff,
        "weighted_robust_accuracy_improvement": robustaccuracyImprove,
        "weighted_natural_f1_score_tradeOff": naturalF1ScoreTradeOff,
        "weighted_robust_f1_score_improvement": robustF1ScoreImprove
      }
    }
    if self.showDetails:
      print('\n')
      print(result)

    return result
  