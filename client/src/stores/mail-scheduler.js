import { defineStore } from 'pinia'
import client from "@/client.js"

export const useMailSchedulerStore = defineStore('mailScheduler', {
  state: () => ({
    loading: false,
    error: null,
    success: false,
    snackbar: {
      show: false,
      message: '',
      color: 'success'
    },
    mailData: {
      recipient_email: '',
      subject: '',
      message: '',
      scheduled_time: ''
    }
  }),

  actions: {
    async scheduleEmail(mailData) {
      this.loading = true
      this.error = null
      this.success = false
      
      try {
        const response = await client.post('schedule-mail/', mailData)
        this.success = true
        this.showSnackbar('Mail scheduled successfully!', 'success')
        this.resetForm()
        return response.data
      } catch (error) {
        const errorMessage = error.response?.data?.message || 'An error occurred while sending mail'
        this.error = errorMessage
        this.showSnackbar(errorMessage, 'error')
        throw error
      } finally {
        this.loading = false
      }
    },

    showSnackbar(message, color = 'success') {
      this.snackbar = {
        show: true,
        message,
        color
      }
    },

    hideSnackbar() {
      this.snackbar.show = false
    },

    resetForm() {
      this.mailData = {
        recipient_email: '',
        subject: '',
        message: '',
        scheduled_time: ''
      }
    },

    clearMessages() {
      this.error = null
      this.success = false
    }
  }
})