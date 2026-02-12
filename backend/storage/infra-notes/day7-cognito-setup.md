# Day 7 – Cognito Setup

User Pool ID: us-east-1_65b7DDtg2
Region: us-east-1
App Client ID: 4jsmm8sikqn8tl8mobfoluana0

Sign-in: Email
Self registration: Enabled
MFA: Disabled
Return URL: http://localhost:3000

## User Groups Created

- admins → Can upload scans
- users → Can only view scans

Role-based access control will be enforced in FastAPI by checking "cognito:groups" from JWT.
