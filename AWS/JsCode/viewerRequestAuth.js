// required libraries
const cookie = require('cookie'); // I use version 0.5.0
const jose = require('jose'); // I use version 4.8.3

// TODO fill config values with outputs from CloudFormation shown later in the article
const config = {
  cognitoUserPoolId: 'us-east-1_fm5dV3KTN',
  cognitoClientId: '2u4l52hhtknq3be1dk6j3pt314',
  cognitoDomainName: 'alisherfreedomaintry'
};

// download jwks.json from https://cognito-idp.eu-west-1.amazonaws.com/${config.cognitoUserPoolId}/.well-known/jwks.json
// according to AWS support, the keys are not rotated so you can do this once and include the file to avoid timeout issues
const jwks = jose.createLocalJWKSet(require('./jwks.json')); 

async function verifyToken(cf) {
  if (cf.request.headers.cookie) {
    const cookies = cookie.parse(cf.request.headers.cookie[0].value);
    try {
      const { payload } = await jose.jwtVerify(cookies.token, jwks, {
        issuer: `https://cognito-idp.eu-west-1.amazonaws.com/${config.cognitoUserPoolId}`
      });
      if (payload.client_id === config.cognitoClientId) {
        return true;
      }
    } catch(err) {
      console.log(`token error: ${err.name} ${err.message}`);
    }
  }
  return false;
}

exports.handler = async function(event) {
  const cf = event.Records[0].cf;

  const valid = await verifyToken(cf);
    if (valid === true) {
      return cf.request;
    } else {
      return {
        status: '302',
        statusDescription: 'Found',
        headers: {
          location: [{ // instructs browser to redirect after receiving the response
            key: 'Location',
            value: `https://${config.cognitoDomainName}.auth.eu-west-1.amazoncognito.com/login?client_id=${config.cognitoClientId}&response_type=code&scope=email+openid&redirect_uri=https%3A%2F%2Falisherfreedomaintry.tk`,
          }]
        }
      };
    }
};