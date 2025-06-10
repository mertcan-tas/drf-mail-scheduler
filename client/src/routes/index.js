import appRoutes from "./app.js";
import generatorRoutes from "./generator.js";
import errorRoutes from "./errors.js";

const allAppRoutes = [...generatorRoutes, ...appRoutes, ...errorRoutes];

export default allAppRoutes;
