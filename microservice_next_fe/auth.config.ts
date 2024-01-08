import type { NextAuthConfig } from 'next-auth';
import Credentials from "next-auth/providers/credentials";
import { LoginSchema } from "@/schemas";

export const authConfig = {

    providers: [
        Credentials({
          async authorize(credentials) {
            const validatedFields = LoginSchema.safeParse(credentials);
    
            if (validatedFields.success) {
                const { username, password } = validatedFields.data;

                const request_form_data = new FormData();
                request_form_data.append('username', username);
                request_form_data.append('password', password);

                const user = await fetch(`${process.env.BACKEND_URL}/api/auth/login`, {
                    method: 'POST',
                    // "content-type": "multipart/form-data", // This line should be removed
                    body: request_form_data
                });
              
                if (!user || user.status !== 200) return null;

                const user_data = await user.json();
    
                return user_data
            }
    
            return null;
          }
        })
      ],
  } satisfies NextAuthConfig;