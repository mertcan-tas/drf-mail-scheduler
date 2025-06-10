const errorRoutes = [
  {
    path: "/:catchAll(.*)",
    redirect: "/",
    name: "notfound",
  },
];

export default errorRoutes;
