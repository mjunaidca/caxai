"use server";

import * as z from "zod";
// import { AuthError } from "next-auth";

// import { db } from "@/lib/db";
// import { signIn } from "@/auth";
import { LoginSchema } from "@/schemas";
// import { getUserByEmail } from "@/data/user";
// import { getTwoFactorTokenByEmail } from "@/data/two-factor-token";
// import {
//   sendVerificationEmail,
//   sendTwoFactorTokenEmail,
// } from "@/lib/mail";
// import { DEFAULT_LOGIN_REDIRECT } from "@/routes";
// import {
//   generateVerificationToken,
//   generateTwoFactorToken
// } from "@/lib/tokens";
// import {
//   getTwoFactorConfirmationByUserId
// } from "@/data/two-factor-confirmation";

export const login = async (values: z.infer<typeof LoginSchema>) => {
  console.log("login", values);

  const validatedFields = LoginSchema.safeParse(values);

  if (!validatedFields.success) {
    return { error: "Invalid fields!" };
  }

  const { email, password, code } = validatedFields.data;

  return { success: "LoggedIn!" }

};
