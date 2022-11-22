<template>
  <div class="reviews">
    <v-row v-for="review in reviews" :key="review.id">
      <v-col cols="3" class="d-flex">
        <img src="@/assets/avatar-1.jpg" alt="avatar" class="avatar">
        <div>
          <div class="author">{{ review.author }}</div>
          <div class="company">{{ review.company }}</div>
        </div>
      </v-col>

      <v-col cols="9">
        <div class="d-flex justify-space-between align-center">
          <v-rating :value="review.rate" readonly dense></v-rating>
          <span class="date">{{ review.date }}</span>
        </div>
        <h3 class="mt-3">{{ review.title }}</h3>
        <p>{{ review.text }}</p>
      </v-col>
    </v-row>

    <v-row class="mt-10">
      <v-col offset="3" cols="9">
        <h3 class="my-3">Write a review</h3>
        <div class="d-flex align-center">
          <span class="mr-2">Rate:</span>
          <v-rating v-model="rate" dense></v-rating>
        </div>
        <div class="form-group">
          <input type="text" class="input-field" v-model="title" placeholder="Topic" />
        </div>
        <div class="form-group">
          <textarea class="area-field" v-model="text" placeholder="Your review" rows="5"></textarea>
        </div>
        <div class="d-flex justify-end">
          <button @click="handleSubmit" class="button submit" :disabled="!isValidForm">Send</button>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
  export default {
    name: "Reviews",
    data() {
      return {
        rate: 4,
        title: '',
        text: '',
        reviews: [
          {
            id: 1,
            author: 'Keanu Reeves',
            company: 'CD Project',
            rate: 4,
            title: 'Very good report',
            text: 'Fitch Solutions rates the overall operational risk of Argentina with 47.8 in 2019, meaning the risk decreased compared to the previous year. Find out more about Argentina in our report focusing on the general economy, trade and investment, society, consumers, retail and eCommerce markets, infrastructure, and politics.',
            date: '12.09.2019, 1:00 PM',
          },
          {
            id: 2,
            author: 'Tom Hardy',
            company: 'Gotham Industries',
            rate: 5,
            title: 'Well prepared',
            text: 'Fitch Solutions rates the overall operational risk of Argentina with 47.8 in 2019, meaning the risk decreased compared to the previous year. Find out more about Argentina in our report focusing on the general.',
            date: '12.09.2019, 1:00 PM',
          },
          {
            id: 3,
            author: 'Mark Darey',
            company: 'Pamberley Inc.',
            rate: 4,
            title: 'Nice!',
            text: 'Fitch Solutions rates the overall operational risk of Argentina with 47.8 in 2019, meaning the risk decreased compared to the previous year. Find out more about Argentina in our report focusing on the general economy, trade and investment, society, consumers, retail and eCommerce markets, infrastructure, and politics.',
            date: '12.09.2019, 1:00 PM',
          }
        ],
      }
    },
    methods: {
      handleSubmit() {
        const payload = {
          id: Math.floor(Math.random() * 100),
          author: 'Alice Kowalewski',
          company: 'Private Inc.',
          rate: this.rate,
          title: this.title,
          text: this.text,
          date: '12.09.2019, 1:00 PM',
        };

        this.reviews.push(payload);

        this.title = '';
        this.rate = 4;
        this.text = '';
      }
    },
    computed: {
      isValidForm() {
        return this.title.length > 0 && this.text.length > 0;
      }
    }
  }
</script>

<style scoped lang="scss">
  .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    box-shadow: 0 2px 10px 0 #dce2e8;
    border: solid 3px #ffffff;
    object-fit: cover;
    margin-right: 20px;
  }
  .author {
    color: #0a1448;
    font-weight: 700;
  }
  .company {
    color: #9296ad;
    font-size: 16px;
    font-weight: 500;
  }

  .form-group {
    margin-bottom: 8px;

    .input-field {
      border-radius: 4px;
      border: solid 1px #dee3ed;
      width: 100%;
      padding: 10px;
      outline: none;
      margin-top: 6px;
      background: #ffffff;
    }

    .area-field {
      border: 1px solid #dee3ed;
      border-radius: 4px;
      width: 100%;
      padding: 4px 10px;
      outline: none;
      margin-top: 6px;
      resize: none;
      background: #ffffff;
    }
  }

  .date {
    color: #38406a;
    font-size: 13px;
  }

  .button {
    outline: none;
    padding: 4px 14px;
    display: flex;
    justify-content: center;
    font-weight: bold;
    font-size: 14px;
    align-items: center;
    border-radius: 4px;

    &.submit {
      color: #ffffff;
      box-shadow: 0 5px 7px 0 rgba(94, 130, 245, 0.24);
      background-image: linear-gradient(to right, #2f6bff, #5e82f5);
    }

    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
  }
</style>
