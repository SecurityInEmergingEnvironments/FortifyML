# Customized score 02
from Interfaces import CustomizedMetricScoreInterface
class CNS01(CustomizedMetricScoreInterface):
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
    initialTime = scoreDictionary['baseline_performance']['inference_elapsed_time_per_1000_in_s']
    addedTime = scoreDictionary['defender_performance']['inference_elapsed_time_per_1000_in_s']

    naturalaccuracyWithoutDefense = scoreDictionary['baseline_performance']['natural_accuracy']
    robustaccuracyWithoutDefense = scoreDictionary['attacker_performance']['robust_accuracy']

    naturalaccuracyWithDefense = scoreDictionary['defender_performance']['natural_accuracy']
    robustaccuracyWithDefense = scoreDictionary['defender_performance']['robust_accuracy']

    timeTradeOff = self.alpha * ((addedTime) / initialTime)
    naturalaccuracyTradeOff = self.beta * ((naturalaccuracyWithDefense - naturalaccuracyWithoutDefense) / naturalaccuracyWithoutDefense)
    robustaccuracyImprove = self.gamma * ((robustaccuracyWithDefense - robustaccuracyWithoutDefense) / robustaccuracyWithoutDefense)

    CNS01_score = ( -timeTradeOff + \
       naturalaccuracyTradeOff + \
         robustaccuracyImprove)

    result = {
      "denoiser_name": scoreDictionary['nameOfDefender'],
      "score": CNS01_score,        # required from users
      "details": {
        "weighted_inference_time_tradeOff": timeTradeOff,
        "weighted_natural_F1_score_tradeOff": naturalaccuracyTradeOff,
        "weighted_robust_F1_score_improvement": robustaccuracyImprove
      }
    }
    if self.showDetails:
      print('\n')
      print(result)

    return result
  