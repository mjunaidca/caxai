import NextAuth from "next-auth";
import { NextResponse } from 'next/server'

import { authConfig } from "@/auth.config";
import {
  DEFAULT_LOGIN_REDIRECT,
  apiAuthPrefix,
  authRoutes,
  publicRoutes,
} from "@/routes";

const { auth } = NextAuth(authConfig);

export default auth((req) => {
  console.log("MIDDLEWARE.TS: PATHNAME", req.nextUrl.pathname);
  const { searchParams } = new URL(req.url);
  
  const redirect_uri = searchParams.get("redirect_uri");
  const response_type = searchParams.get("response_type");
  const client_id = searchParams.get("client_id");
  const scope = searchParams.get("scope");
  const state = searchParams.get("state");

  const { nextUrl } = req;
  const isLoggedIn = !!req.auth;

  const isApiAuthRoute = nextUrl.pathname.startsWith(apiAuthPrefix);
  const isPublicRoute = publicRoutes.includes(nextUrl.pathname);
  const isAuthRoute = authRoutes.includes(nextUrl.pathname);

  if (isApiAuthRoute) {
    return null;
  }

  if (isAuthRoute) {
    if (isLoggedIn) {
      if (redirect_uri && state) {
        const redirctNewUrl = DEFAULT_LOGIN_REDIRECT + `?redirect_uri=${redirect_uri}`  + `&state=${state}` + `&response_type=${response_type}` + `&client_id=${client_id}` + `&scope=${scope}`
        return NextResponse.redirect(new URL(redirctNewUrl, nextUrl));
      } else {
        return NextResponse.redirect(new URL(DEFAULT_LOGIN_REDIRECT, nextUrl));
      }
    }
    return null;
  }

  if (!isLoggedIn && !isPublicRoute) {
    let callbackUrl = nextUrl.pathname;
    if (nextUrl.search) {
      callbackUrl += nextUrl.search;
    }

    const encodedCallbackUrl = encodeURIComponent(callbackUrl);

    return NextResponse.redirect(
      new URL(`/auth/login?callbackUrl=${encodedCallbackUrl}`, nextUrl)
    );
  }

  return null;
});

// Optionally, don't invoke Middleware on some paths
export const config = {
  matcher: ["/((?!.+\\.[\\w]+$|_next).*)", "/"],
};
