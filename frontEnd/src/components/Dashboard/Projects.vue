<template>
  <div class="projects">
    <div class="d-flex justify-space-between">
      <div class="d-flex align-center flex-grow-1">
        <GridIcon class="icon active" />
        <BurgerIcon class="icon mx-4" />
        <v-select
          class="sort mx-8"
          :items="sortItems"
          v-model="selected"
          @change="sortBy"
          solo
        ></v-select>
      </div>
      <div class="d-flex align-center flex-grow-1">
        <div class="search-container">
          <SearchIcon class="search-icon" />
          <input type="search" class="search" v-model="search" placeholder="Search for items" />
        </div>
        <button class="add-button">
          <PlusIcon class="mr-4"/> Add project
        </button>
      </div>
    </div>

    <v-row class="mt-8">
      <v-col lg="4" md="6" sm="6" xs="12" :key="project.id" v-for="project in filteredProjects">
        <div class="project-card pa-3">
          <div class="card-content">
            <div class="d-flex">
              <div class="light-container mr-2">
                <div class="light-icon"></div>
              </div>
              <div class="project-title">{{ project.title }}</div>
            </div>
            <div class="d-flex justify-end mx-1">
              <span class="label">{{ project.updated }}</span>
            </div>
          </div>

          <div class="card-footer">
            <span class="card-owner">Owner: {{ project.owner }}</span>
            <div class="d-flex align-center">
              <img class="avatar" src="@/assets/avatar-1.jpg" alt="avatar">
              <img class="avatar" src="@/assets/avatar-2.jpg" alt="avatar">
              <img class="avatar" src="@/assets/avatar-3.jpg" alt="avatar">
              <img class="avatar" src="@/assets/avatar-4.jpg" alt="avatar">
            </div>
          </div>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
  import GridIcon from '@/assets/icons/grid.svg';
  import BurgerIcon from '@/assets/icons/burger.svg';
  import SearchIcon from '@/assets/icons/search.svg';
  import PlusIcon from '@/assets/icons/plus.svg';

  export default {
    name: "Projects",
    components: {
      GridIcon,
      BurgerIcon,
      SearchIcon,
      PlusIcon,
    },
    data() {
      return {
        search: '',
        isTableView: false,
        selected: 'updated',
        sortItems: [{ text: 'Last updated', value: 'updated'}, { text: 'Name', value: 'title' }],
        projects: [
          { id: 1, title: 'Bank Dataset', updated: '1 day ago', owner: 'Abdullah Ali' },
          // { id: 2, title: 'New York apartments price predictor', updated: '2 days ago', owner: 'Tomasz Drozdowicz' },
          // { id: 3, title: 'Face recognition', updated: '3 days ago', owner: 'Me' },
          // { id: 4, title: 'Restaurant violance prodtions for next 10 yrs', updated: '1 day ago', owner: 'John Smith' },
        ]
      }
    },
    computed: {
      filteredProjects() {
        return this.projects.filter((item) => item.title.toLowerCase().includes(this.search.toLowerCase()));
      },
    },
    methods: {
      sortBy(field) {
        this.projects.sort((a, b) => a[field] < b[field] ? -1 : 1);
      },
    }
  }
</script>

<style scoped lang="scss">
  .projects {
    // background-color: #f4f6fa;

    .icon {
      width: 17px;
      height: 17px;
      cursor: pointer;

      &.active {
        g {
          fill: #2f6bff;
        }
      }
    }

    .sort {
      max-width: 200px;
      height: 42px;
    }

    .search-container {
      display: flex;
      position: relative;
      height: 42px;
      margin-right: 20px;
      flex: 1;

      .search-icon {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        left: 10px;
      }

      .search {
        background-color: #ffffff;
        box-sizing: border-box;
        height: 42px;
        outline: none;
        padding: 18px 18px 18px 30px;
        border-radius: 4px;
        border: solid 1px #dee3ed;
        color: #858ba0;
        font-size: 14px;
        width: 100%;
      }
    }

    .add-button {
      height: 42px;
      width: 162px;
      color: #ffffff;
      outline: none;
      border-radius: 4px;
      box-shadow: 0 5px 7px 0 rgba(94, 130, 245, 0.24);
      background-image: linear-gradient(to right, #2f6bff, #5e82f5);
      padding: 8px 16px;
      display: flex;
      font-weight: bold;
      font-size: 14px;
      align-items: center;
    }

    .project-card {
      border-radius: 4px;
      box-shadow: 0 13px 12px 0 #eaedf4;
      background-color: #ffffff;
      min-height: 165px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;

      .project-title {
        color: #0a1448;
        font-size: 17px;
        font-weight: bold;
      }

      .label {
        color: #858ba0;
        font-size: 13px;
        border-radius: 3px;
        background-color: #f4f6fa;
        padding: 2px 8px;
        min-width: 82px;
        height: 26px;
      }

      .card-content {
        display: flex;
        flex: 2;
        justify-content: space-between;

        .light-container {
          width: 21px;
          height: 21px;
          padding: 4px;
          background-color: rgb(13, 200, 134, 0.21);
          border-radius: 13.5px;
          display: flex;
          align-items: center;
          justify-content: center;

          .light-icon {
            width: 11px;
            height: 11px;
            opacity: 1;
            background-color: #0dc886;
            border-radius: 7px;
          }
        }
      }

      .card-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 12px;
        border-top: 1px solid #f4f6fa;

        .card-owner {
          color: #858ba0;
          font-size: 13px;
        }

        .avatar {
          width: 23px;
          height: 23px;
          border-radius: 50%;
          box-shadow: 0 2px 10px 0 #dce2e8;
          border: solid 3px #ffffff;
          object-fit: cover;
        }
      }
    }
  }
</style>
