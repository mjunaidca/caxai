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

  console.log(
    "middleware.ts: searchParams",
    searchParams
  );
  

  const redirect_uri = searchParams.get("redirect_uri");
  const response_type = searchParams.get("response_type");
  const client_id = searchParams.get("client_id");
  const scope = searchParams.get("scope");
  const state = searchParams.get("state");

  console.log("middleware.ts REDIRECT_URI", redirect_uri); // 'https://chat.openai.com/aip/g-8a12b72cbad2ac62a38cbda91d8d14d3ad677cdf/oauth/callback'
  

  // if redirect_uri: 'https://chat.openai.com/aip/g-8a12b72cbad2ac62a38cbda91d8d14d3ad677cdf/oauth/callback'
  // if User is LoggedIn then get access_token and refresh_token
  // if User is not LoggedIn then redirect to login page to login
  // We have to use oAuth protocol and send user back to the above redirect_uri with access_token

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
        const redirctNewUrl = DEFAULT_LOGIN_REDIRECT + `?redirect_uri=${redirect_uri}` + `&response_type=${response_type}` + `&client_id=${client_id}` + `&scope=${scope}` + `&state=${state}`
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
