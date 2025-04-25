from flask import g, jsonify
from functools import wraps



def prompt_scoring(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
          parsed_user_query = g.parsed_user_query
          # weights for each field value of 1-5 - 5 being highest weight
          field_weights = {
            'task': 4,
            'role': 3,
            'context': 2,
            'rules': 3,
            'examples': 2,
            'format': 2,
            'word_count': 3
          }
          score = 0
          max_possible_score = 0
          score_by_field = {}
          
          for key in field_weights:
            weight = field_weights[key]
            max_possible_score += weight
            
            if key == 'word_count': 
              continue
            
            if parsed_user_query[key]:
              score += weight
              score_by_field[key] = weight
            else:
              score_by_field[key] = 0
          word_count_score = get_word_count_score(parsed_user_query['word_count'], field_weights['word_count'])
          score_by_field['word_count'] = word_count_score
          score += word_count_score
          percentage_score = (score / (max_possible_score + field_weights['word_count'])) * 100
          
          g.total_score = score
          g.max_possible_score = max_possible_score
          g.percentage_score = percentage_score
          g.score_by_field = score_by_field
          return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    return wrapper
  
  
def get_word_count_score(query_word_count, weight): 
      min_ideal_word_count = 100
      max_ideal_word_count = 300
      
      if query_word_count > min_ideal_word_count and query_word_count < max_ideal_word_count:
        return weight
      elif query_word_count < min_ideal_word_count:
        return (query_word_count / min_ideal_word_count) * weight
      else:
        over_limit = min(1, (max_ideal_word_count / query_word_count))
        return (weight * over_limit)