import * as z from "zod";


export const LoginSchema = z.object({
  username: z.string().min(1, {
    message: "Username is required",
  }),
  password: z.string().min(1, {
    message: "Password is required",
  }),
  code: z.optional(z.string()),
});

export const RegisterSchema = z.object({
  email: z.string().email({
    message: "Email is required",
  }),
  password: z.string().min(6, {
    message: "Minimum 6 characters required",
  }),
  username: z.string().min(1, {
    message: "UserName is required",
  }),
  fullname: z.string().min(1, {
    message: "FullName is required",
  }),
});
