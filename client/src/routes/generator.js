const generatorRoutes = [
  {
    path: "/django-secret-key",
    name: "django-secret",
    component: () => import("@/views/gens/django/DjangoSecretGen.vue"),
  },
  {
    path: "/fernet-key",
    name: "fernet",
    component: () => import("@/views/gens/fernet/FernetGen.vue"),
  },
];

export default generatorRoutes;
