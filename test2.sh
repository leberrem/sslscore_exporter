python -u ssllabs-cli.py --use-cache github.com |jq ".endpoints[] | [.grade, .ipAddress]"

python -u httpobs-cli.py github.com -d |jq ".scan | [.score, .grade]"
