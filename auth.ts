import NextAuth from "next-auth";
import { authConfig } from "@/auth.config";

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
    async jwt({ token, user }) {
      // Convert the user object to unknown first, then to ExtendedUserResponse
      const extendedUserResponse = user as unknown as ExtendedUserResponse | null;
    
      if (extendedUserResponse?.user) {
        const extendedUser = extendedUserResponse.user;
        token.id = extendedUser.id;
        token.name = extendedUser.full_name;
        token.email = extendedUser.email;
        token.emailVerified = extendedUser.email_verified;
      }
    
      if (extendedUserResponse?.access_token) {
        token.accessToken = extendedUserResponse.access_token;
      }
    
      return token;
    },
    

    async session({ session, token }) {
      if (token) {
        session.user = {
          id: token.id as unknown as string,
          name: token.name,
          email: token.email,
          // @ts-ignore
          emailVerified: token.emailVerified,
          accessToken: token.accessToken, // Added access token to session
        };
      }
      return session;
    },
  },

  session: { strategy: "jwt" },
  ...authConfig,
});
