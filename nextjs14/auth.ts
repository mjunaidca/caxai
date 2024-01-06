import NextAuth from "next-auth";
import { authConfig } from "@/auth.config";

// Custom types to handle the additional properties in your API response
interface ExtendedUser {
  id: string;
  username: string;
  email: string;
  full_name: string;
  email_verified: boolean;
}

interface ExtendedAccount {
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
    async jwt({ token, user, account }) {
      const extendedUser = user as ExtendedUser;
      const extendedAccount = account as ExtendedAccount;

      if (extendedAccount && extendedUser) {
        token.accessToken = extendedAccount.access_token;
        token.id = extendedUser.id; // Already a string, no assertion needed
        token.name = extendedUser.full_name;
        token.email = extendedUser.email;
        token.emailVerified = extendedUser.email_verified; // Already a boolean, no assertion needed
      }

      return token;
    },

    async session({ session, token }) {
      session.user = {
        ...session.user,
        id: token.id as string, // Type assertion for string
        name: token.name, // Assuming it's already a string
        email: token.email, // Assuming it's already a string
      };
      return session;
    },
    // signIn callback is not needed if you're directly handling it in authConfig
  },

  session: { strategy: "jwt" },
  ...authConfig,
});
