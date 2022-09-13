// required libraries
const querystring = require('querystring'); // included in Node.js
const cookie = require('cookie'); // I use version 0.5.0
const axios = require('axios'); // I use version 0.27.2

// TODO fill config values with outputs from CloudFormation shown later in the article
const config = {
  cognitoClientId: '',
  cognitoClientSecret: '',
  cognitoDomainName: ''
};

exports.handler = async function(event) {
  const cf = event.Records[0].cf;
  if (cf.request.uri.startsWith('/')) {
    const {code} = querystring.parse(qs);
    const res = await axios({
      method: 'POST',
      headers: {
        'content-type': 'application/x-www-form-urlencoded',
        authorization: 'Basic ' + Buffer.from(config.cognitoClientId + ':' + config.cognitoClientSecret).toString('base64')
      },
      data: querystring.stringify({
        grant_type: 'authorization_code',
        redirect_uri: 'https://alisherfreedomaintry.tk',
        code
      }),
      url: `https://${config.cognitoDomainName}.auth.eu-west-1.amazoncognito.com/oauth2/token`,
    });
    if (res.status === 200) {
      const setCookieValue = cookie.serialize('token', res.data.access_token, {
        maxAge: res.data.expires_in,
        path: '/',
        secure: true
      });
      return {
        status: '302',
        headers: {
          location: [{ // instructs browser to redirect after receiving the response
          	key: 'Location',
          	value: '/'
          }],
          'set-cookie': [{ // instructs browser to store a cookie
          	key: 'Set-Cookie',
          	value: setCookieValue
          }],
          'cache-control': [{ // ensures that CloudFront does not cache the response
          	key: 'Cache-Control',
          	value: 'no-cache'
          }]
        }
      };
    } else {
      throw new Error('unexpected status code: ' + res.status);
    }
  }
  // do nothing: CloudFront continues as usual
  return cf.request;
};