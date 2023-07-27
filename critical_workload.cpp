#include <stdio.h>
#include <pqos.h>

// Define the function representing the critical workload
void criticalWorkload() {
    // Simulate some intensive computations
    for (int i = 0; i < 1000000; ++i) {
        for (int j = 0; j < 1000; ++j) {
            double result = i * j * 1.5;
        }
    }
}


int main() {
    int ret;
    struct pqos_cap *cap = NULL;
    struct pqos_cpuinfo *cpu = NULL;
    const struct pqos_capability *cap_cat = NULL;
    unsigned cat_id;
    unsigned num_cos;
    struct pqos_cos *cos_tab = NULL;
    unsigned l3_cache_size;

    ret = pqos_init(NULL);
    if (ret != PQOS_RETVAL_OK) {
        printf("Error initializing PQoS library!\n");
        return -1;
    }

    ret = pqos_cap_get(&cap, &cpu);
    if (ret != PQOS_RETVAL_OK) {
        printf("Error getting PQoS capabilities!\n");
        pqos_fini();
        return -1;
    }

    cap_cat = pqos_cap_get_type(cap, PQOS_CAP_TYPE_L3CA);
    if (cap_cat == NULL) {
        printf("L3 CAT capability not detected!\n");
        pqos_fini();
        return -1;
    }

    l3_cache_size = cap_cat->u.l3ca->num_ways;

    num_cos = cap_cat->u.l3ca->num_classes;
    cos_tab = (struct pqos_cos *)malloc(num_cos * sizeof(struct pqos_cos));
    if (cos_tab == NULL) {
        printf("Error allocating COS table memory!\n");
        pqos_fini();
        return -1;
    }

    for (cat_id = 0; cat_id < num_cos; cat_id++) {
        ret = pqos_alloc_assoc_get(cos_tab + cat_id, cat_id);
        if (ret != PQOS_RETVAL_OK) {
            printf("Error getting COS association!\n");
            free(cos_tab);
            pqos_fini();
            return -1;
        }
    }

    // Assign 50% of the cache (ways) to COS 1
    unsigned cat_mask = (1ULL << (l3_cache_size / 2)) - 1;
    ret = pqos_l3ca_set(cat_id, cat_mask, 1, 0);
    if (ret != PQOS_RETVAL_OK) {
        printf("Error setting L3 CAT allocation!\n");
        free(cos_tab);
        pqos_fini();
        return -1;
    }

    printf("Successfully allocated 50%% of L3 cache to COS 1.\n");

    // Call the critical workload to execute with the allocated cache
    criticalWorkload();

    // Cleanup
    free(cos_tab);
    pqos_fini();

    return 0;
}
