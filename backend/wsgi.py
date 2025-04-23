import os
from app import create_app

config_type = os.environ.get('FLASK_CONFIG', 'DEV')

if config_type == 'DEV':
  config_class = 'config.DevelopmentConfig'
elif config_type == 'TEST':
  config_class = 'config.TestingConfig'
elif config_type == 'PROD':
  config_class = 'config.ProductionConfig'
else:
  # default to dev
  config_class = 'config.DevelopmentConfig'

app = create_app(config_class)


if __name__ == '__main__':
  app.run()
