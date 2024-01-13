import NextAuth from "next-auth";
import { authConfig } from "@/auth.config";
import { refreshToken } from "./actions/refresh-token";

interface ExtendedUserResponse {
  user: {
    id: string;
    username: string;
    email: string;
    full_name: string;
    email_verified: boolean;
  };
  access_token: string;
  token_type: string;
  expires_in: number;
  refresh_token: string;
  accessTokenExpires: number; // Custom property returned with the user object
}

export const {
  handlers: { GET, POST },
  auth,
  signIn,
  signOut,
  update,
} = NextAuth({
  pages: {
    signIn: "/auth/login",
    error: "/auth/error",
  },
  callbacks: {
    async jwt({ token, user }: any) {
      // Convert the user object to unknown first, then to ExtendedUserResponse
      const extendedUserResponse =
        user as unknown as ExtendedUserResponse | null;

      if (extendedUserResponse?.user) {
        const extendedUser = extendedUserResponse.user;
        token.id = extendedUser.id;
        token.name = extendedUser.full_name;
        token.email = extendedUser.email;
        token.emailVerified = extendedUser.email_verified;
      }

      if (extendedUserResponse?.access_token) {
        token.accessToken = extendedUserResponse.access_token;
        token.refreshToken = extendedUserResponse.refresh_token;
        token.expires_in = extendedUserResponse.expires_in;
        token.accessTokenExpires = extendedUserResponse.accessTokenExpires; // Use the accessTokenExpires value from the login response
      }
      return token;
    },

    async session({ session, token }: any) {
      if (token) {
        session.user = {
          id: token.id as unknown as string,
          name: token.name,
          email: token.email,
          emailVerified: token.emailVerified,
          accessToken: token.accessToken, // Added access token to session
          refreshToken: token.refreshToken, // Added refresh token to session
          expires_in: token.expires_in,
          accessTokenExpires: token.accessTokenExpires,
        };

        // If Access token has expired, try to refresh it
        if (token.accessTokenExpires < Date.now()) {
          try {
            console.log("Refreshing access token");
            console.log(token.accessTokenExpires < Date.now());

            const refreshedTokens = await refreshToken(token.refreshToken);

            console.log(refreshedTokens);

            // Add the new accessToken and refreshToken to the session
            session.user.accessToken = refreshedTokens.access_token;
            session.user.refreshToken = refreshedTokens.refresh_token;
            session.user.accessTokenExpires = refreshedTokens.expires_in * 1000; // Convert to milliseconds
          } catch (error) {
            console.error("Token refresh failed:");
            // Handle token refresh failure (e.g., redirect to login)
            console.log("FAILED TO REFRESH TOKEN");

            console.log("Redirecting to login");

            throw new Error("TokenRefreshFailed");
          }
        }
      }

      return session;
    },
  },

  session: { strategy: "jwt" },
  ...authConfig,
});
