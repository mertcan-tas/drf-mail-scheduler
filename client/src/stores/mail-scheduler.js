import { defineStore } from "pinia";
import client from "@/client.js";

export const useMailSchedulerStore = defineStore("mailScheduler", {
  state: () => ({
    loading: false,
    error: null,
    success: false,
    snackbar: {
      show: false,
      message: "",
      color: "success",
    },
    mailData: {
      recipient_email: "",
      subject: "",
      message: "",
      scheduled_time: "",
    },
  }),

  actions: {
    async scheduleEmail(mailData) {
      this.loading = true;
      this.error = null;
      this.success = false;

      try {
        const scheduledTime = new Date(mailData.scheduled_time);
        const now = new Date();

        if (scheduledTime <= now) {
          throw new Error("The submission time must be in the future.");
        }

        const response = await client.post("schedule-mail/", mailData);
        this.success = true;
        this.showSnackbar("Mail scheduled successfully!", "success");
        return response.data;
      } catch (error) {
        let errorMessage = "An error occurred while scheduling email";

        if (error.message === "The submission time must be in the future.") {
          errorMessage = error.message;
        } else if (error.response?.data?.scheduled_time) {
          errorMessage = Array.isArray(error.response.data.scheduled_time)
            ? error.response.data.scheduled_time[0]
            : error.response.data.scheduled_time;
        } else if (error.response?.data?.message) {
          errorMessage = error.response.data.message;
        } else if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail;
        }

        this.error = errorMessage;
        this.showSnackbar(errorMessage, "error");
        throw error;
      } finally {
        this.loading = false;
      }
    },

    showSnackbar(message, color = "success") {
      this.snackbar = {
        show: true,
        message,
        color,
      };
    },

    hideSnackbar() {
      this.snackbar.show = false;
    },

    resetForm() {
      this.mailData = {
        recipient_email: "",
        subject: "",
        message: "",
        scheduled_time: "",
      };
    },

    clearMessages() {
      this.error = null;
      this.success = false;
      this.hideSnackbar();
    },
  },
});