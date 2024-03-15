interface UserData {
  access_token: string;
  token_type: string;
  user: {
    username: string;
    email: string;
    full_name: string;
    email_verified: boolean;
    id: string;
  };
  expires_in: number;
  refresh_token: string;
  accessTokenExpires: number;
}
