<template>
  <Layout>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8" lg="6">
          <v-card elevation="4" class="pa-6">
            <v-card-title class="text-h5 text-center mb-4">
              <v-icon left color="primary">mdi-email-send-outline</v-icon>
              Email Scheduler
            </v-card-title>

            <v-card-text>
              <v-form ref="form" v-model="valid" lazy-validation>
                <v-text-field
                  v-model="mailData.recipient_email"
                  label="Recipient Email Address"
                  :rules="emailRules"
                  prepend-inner-icon="mdi-email"
                  variant="outlined"
                  required
                  class="mb-3 mt-7"
                ></v-text-field>

                <v-text-field
                  v-model="mailData.subject"
                  label="Subject"
                  :rules="subjectRules"
                  prepend-inner-icon="mdi-format-title"
                  variant="outlined"
                  required
                  class="mb-3"
                ></v-text-field>

                <v-textarea
                  v-model="mailData.message"
                  label="Message"
                  :rules="messageRules"
                  prepend-inner-icon="mdi-message-text"
                  variant="outlined"
                  rows="4"
                  required
                  class="mb-3"
                ></v-textarea>

                <v-row>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="dateFormatted"
                      label="Date"
                      prepend-inner-icon="mdi-calendar"
                      variant="outlined"
                      readonly
                      @click="dateDialog = true"
                      :rules="dateRules"
                      required
                    ></v-text-field>
                    <v-dialog v-model="dateDialog" max-width="400px">
                      <v-card>
                        <v-date-picker
                          v-model="selectedDate"
                          :min="new Date().toISOString().substr(0, 10)"
                          show-adjacent-months
                        ></v-date-picker>
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn text @click="dateDialog = false">Cancel</v-btn>
                          <v-btn color="primary" @click="selectDate"
                            >Select</v-btn
                          >
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                  </v-col>

                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="selectedTime"
                      label="Time (HH:MM)"
                      prepend-inner-icon="mdi-clock"
                      variant="outlined"
                      type="time"
                      :rules="timeRules"
                      required
                      placeholder="14:30"
                      hint="24-hour format (e.g. 14:30)"
                      persistent-hint
                    ></v-text-field>
                  </v-col>
                </v-row>

                <v-select
                  v-model="selectedTimezone"
                  :items="timezoneOptions"
                  label="Timezone"
                  prepend-inner-icon="mdi-earth"
                  variant="outlined"
                  class="mb-1 mt-5"
                ></v-select>

                <v-alert
                  v-if="scheduledDateTime"
                  type="info"
                  variant="tonal"
                  class="mb-4"
                >
                  <template v-slot:prepend>
                    <v-icon>mdi-clock-outline</v-icon>
                  </template>
                  <strong>Scheduled Time:</strong> {{ formatScheduledTime }}
                </v-alert>

                <v-alert
                  v-if="error"
                  type="error"
                  variant="tonal"
                  dismissible
                  @click:close="clearMessages"
                  class="mb-4"
                >
                  {{ error }}
                </v-alert>

                <v-alert
                  v-if="success"
                  type="success"
                  variant="tonal"
                  dismissible
                  @click:close="clearMessages"
                  class="mb-4"
                >
                  Email scheduled successfully!
                </v-alert>
              </v-form>
            </v-card-text>

            <v-card-actions class="px-6 pb-6">
              <v-spacer></v-spacer>
              <v-btn-outlined @click="resetForm" :disabled="loading">
                Clear
              </v-btn-outlined>
              <v-btn-primary
                @click="submitForm"
                :loading="loading"
                :disabled="!valid"
                class="ml-2"
              >
                <v-icon left>mdi-send</v-icon>
                Schedule Email
              </v-btn-primary>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>


      <v-snackbar
        v-model="snackbar.show"
        :color="snackbar.color"
        :timeout="4000"
        location="bottom"
        rounded="pill"
        class="mb-5"
      >
        <template v-slot:prepend>
          <v-icon>
            {{
              snackbar.color === "success"
                ? "mdi-check-circle"
                : "mdi-alert-circle"
            }}
          </v-icon>
        </template>
        {{ snackbar.message }}
        <template v-slot:actions>
          <v-btn variant="text" @click="hideSnackbar"> Close </v-btn>
        </template>
      </v-snackbar>
    </v-container>
  </Layout>
</template>

<script>
import { useMailSchedulerStore } from "@/stores/mail-scheduler.js";

export default {
  name: "MailScheduler",
  data() {
    return {
      valid: false,
      dateDialog: false,
      timeDialog: false,
      selectedDate: null,
      selectedTime: null,
      selectedTimezone: "Europe/Istanbul",

      timezoneOptions: [
        { title: "İstanbul (GMT+3)", value: "Europe/Istanbul" },
        { title: "Ankara (GMT+3)", value: "Europe/Istanbul" },
        { title: "UTC (GMT+0)", value: "UTC" },
        { title: "Londra (GMT+0)", value: "Europe/London" },
        { title: "New York (GMT-5)", value: "America/New_York" },
        { title: "Los Angeles (GMT-8)", value: "America/Los_Angeles" },
        { title: "Tokyo (GMT+9)", value: "Asia/Tokyo" },
        { title: "Dubai (GMT+4)", value: "Asia/Dubai" },
      ],

      emailRules: [
        (v) => !!v || "Email is required",
        (v) => /.+@.+\..+/.test(v) || "Please enter a valid email address",
      ],
      subjectRules: [
        (v) => !!v || "Subject is required",
        (v) => (v && v.length >= 3) || "Subject must be at least 3 characters",
      ],
      messageRules: [
        (v) => !!v || "Message is required",
        (v) => (v && v.length >= 3) || "Message must be at least 3 characters",
      ],
      dateRules: [(v) => !!v || "Date selection is required"],
      timeRules: [(v) => !!v || "Time selection is required"],
    };
  },

  computed: {
    mailSchedulerStore() {
      return useMailSchedulerStore();
    },

    mailData: {
      get() {
        return this.mailSchedulerStore.mailData;
      },
      set(value) {
        this.mailSchedulerStore.mailData = value;
      },
    },

    loading() {
      return this.mailSchedulerStore.loading;
    },

    error() {
      return this.mailSchedulerStore.error;
    },

    success() {
      return this.mailSchedulerStore.success;
    },

    snackbar() {
      return this.mailSchedulerStore.snackbar;
    },

    dateFormatted() {
      if (!this.selectedDate) return "";
      const date = new Date(this.selectedDate);
      return date.toLocaleDateString("tr-TR");
    },

    timeFormatted() {
      if (!this.selectedTime) return "";
      return this.selectedTime;
    },

    scheduledDateTime() {
      if (!this.selectedDate || !this.selectedTime) return null;

      const dateStr =
        typeof this.selectedDate === "string"
          ? this.selectedDate
          : this.selectedDate.toISOString().split("T")[0];
      const [hours, minutes] = this.selectedTime.split(":");

      const localDateTime = new Date(`${dateStr}T${this.selectedTime}:00`);

      const utcDateTime = this.convertToUTC(
        localDateTime,
        this.selectedTimezone
      );

      return utcDateTime.toISOString();
    },

    formatScheduledTime() {
      if (!this.scheduledDateTime) return "";

      const date = new Date(this.scheduledDateTime);
      return date.toLocaleString("tr-TR", {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },
  },

  watch: {
    scheduledDateTime(newValue) {
      if (newValue) {
        this.mailData.scheduled_time = newValue;
      }
    },
  },

  methods: {
    selectDate() {
      this.dateDialog = false;
    },

    convertToUTC(localDateTime, timezone) {
      const tempDate = new Date(
        localDateTime.toLocaleString("en-US", { timeZone: timezone })
      );
      const utcDate = new Date(
        localDateTime.toLocaleString("en-US", { timeZone: "UTC" })
      );
      const offset = utcDate.getTime() - tempDate.getTime();

      return new Date(localDateTime.getTime() + offset);
    },

    hideSnackbar() {
      this.mailSchedulerStore.hideSnackbar();
    },

    async submitForm() {
      const { valid } = await this.$refs.form.validate();

      if (valid && this.scheduledDateTime) {
        try {
          await this.mailSchedulerStore.scheduleEmail({
            recipient_email: this.mailData.recipient_email,
            subject: this.mailData.subject,
            message: this.mailData.message,
            scheduled_time: this.scheduledDateTime,
          });

          this.resetFormData();
        } catch (error) {
          console.error("Email scheduling error:", error);
        }
      }
    },

    resetForm() {
      this.mailSchedulerStore.resetForm();
      this.resetFormData();
      this.$refs.form.resetValidation();
    },

    resetFormData() {
      this.selectedDate = null;
      this.selectedTime = "";
      this.selectedTimezone = "Europe/Istanbul";
    },

    clearMessages() {
      this.mailSchedulerStore.clearMessages();
    },
  },
};
</script>

<style scoped>
.v-card {
  border-radius: 12px;
}

.v-card-title {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin: -24px -24px 24px -24px;
  padding: 24px;
  border-radius: 12px 12px 0 0;
}
</style>
