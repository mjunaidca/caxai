type SessionUser = {
    id: string;
    name: string;
    email: string;
    emailVerified: boolean;
    accessToken: string;
  };
  
type CustomSession = {
    user: SessionUser;
    expires: string;
  };