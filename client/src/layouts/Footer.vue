<template>
  <v-footer app height="40" class="border-t-thin">
    <a
      v-for="item in items"
      :key="item.title"
      class="d-inline-block mx-2 social-link"
      :href="item.href"
      rel="noopener noreferrer"
      target="_blank"
      :title="item.title"
    >
      <v-icon :icon="item.icon" :size="item.icon === '$vuetify' ? 24 : 16" />
    </a>
    
    <div
      class="text-caption text-disabled"
      style="position: absolute; right: 16px"
    >
      &copy; {{ new Date().getFullYear() }}
      <span class="d-none d-sm-inline-block">Mertcan Taş</span>
      —
      <a
        class="text-decoration-none on-surface"
        href="https://github.com/mertcan-tas/drf-mail-scheduler/blob/master/README.md"
        rel="noopener noreferrer"
        target="_blank"
      >
        MIT License
      </a>
    </div>
  </v-footer>
</template>

<script setup>
const items = [
  {
    title: "Linkedin",
    icon: "mdi-linkedin",
    href: "https://www.linkedin.com/in/mertcan-tas/",
  },
  {
    title: "GitHub",
    icon: `mdi-github`,
    href: "https://github.com/mertcan-tas",
  },
];
</script>

<style scoped lang="sass">
.social-link :deep(.v-icon)
  color: rgba(var(--v-theme-on-background), var(--v-disabled-opacity))
  text-decoration: none
  transition: .2s ease-in-out

  &:hover
    color: rgba(25, 118, 210, 1)
</style>
