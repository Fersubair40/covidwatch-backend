set -e
git remote set-url staging https://git.heroku.com/covidwatch-backend-staging.git
git remote set-url production https://git.heroku.com/covidwatch-backend.git

LIVE_OR_STAGING=$1
if [ -z "$LIVE_OR_STAGING" ]; then
  echo "ERROR: production|staging not selected"
  echo ""
  exit 1
fi
if [ "$LIVE_OR_STAGING" = "staging" ]; then
    git subtree push --prefix cen staging master
    exit 0
fi
if [ "$LIVE_OR_STAGING" = "production" ]; then
    git subtree push --prefix cen production master
    exit 0
fi

echo "ERROR: first arg must be either staging or production"
echo ""
exit 1