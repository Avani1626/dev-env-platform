const cognitoConfig = {
  domain: "https://devplatform123.auth.us-east-1.amazoncognito.com.auth.us-east-1.amazoncognito.com",
  clientId: "3ag53fg3iotu032h6tohf5c5pt",
  redirectUri: "http://localhost:3000",
  responseType: "code",
  scope: "openid email"
};

export const login = () => {
  const loginUrl =
    `https://${cognitoConfig.domain}/oauth2/authorize` +
    `?client_id=${cognitoConfig.clientId}` +
    `&response_type=${cognitoConfig.responseType}` +
    `&scope=${cognitoConfig.scope}` +
    `&redirect_uri=${cognitoConfig.redirectUri}`;

  window.location.href = loginUrl;
};
