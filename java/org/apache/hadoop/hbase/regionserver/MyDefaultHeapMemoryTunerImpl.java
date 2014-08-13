package org.apache.hadoop.hbase.regionserver;

import static org.apache.hadoop.hbase.regionserver.HeapMemoryManager.BLOCK_CACHE_SIZE_MAX_RANGE_KEY;
import static org.apache.hadoop.hbase.regionserver.HeapMemoryManager.BLOCK_CACHE_SIZE_MIN_RANGE_KEY;
import static org.apache.hadoop.hbase.HConstants.HFILE_BLOCK_CACHE_SIZE_KEY;
import static org.apache.hadoop.hbase.regionserver.HeapMemoryManager.MEMSTORE_SIZE_MAX_RANGE_KEY;
import static org.apache.hadoop.hbase.regionserver.HeapMemoryManager.MEMSTORE_SIZE_MIN_RANGE_KEY;

import org.apache.hadoop.classification.InterfaceAudience;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HConstants;
import org.apache.hadoop.hbase.regionserver.HeapMemoryManager.TunerContext;
import org.apache.hadoop.hbase.regionserver.HeapMemoryManager.TunerResult;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.io.*;

/**
* The default implementation for the HeapMemoryTuner. This will do simple checks to decide
* whether there should be changes in the heap size of memstore/block cache. When there is no block
* cache eviction at all but there are flushes because of global heap pressure, it will increase the
* memstore heap size and decrease block cache size. The step value for this heap size change can be
* specified using the config <i>hbase.regionserver.heapmemory.autotuner.step</i>. When there is no
* memstore flushes because of heap pressure but there is block cache evictions it will increase the
* block cache heap.
*/
@InterfaceAudience.Private
class MyDefaultHeapMemoryTunerImpl implements HeapMemoryTuner {

  public static final String STEP_KEY = "hbase.regionserver.heapmemory.autotuner.step";
  public static final float DEFAULT_STEP_VALUE = 0.05f; // 10%

  private static final TunerResult TUNER_RESULT = new TunerResult(true);
  private static final TunerResult NO_OP_TUNER_RESULT = new TunerResult(false);

  private Configuration conf;
  private float step = DEFAULT_STEP_VALUE;

  private float globalMemStorePercentMinRange;
  private float globalMemStorePercentMaxRange;
  private float blockCachePercentMinRange;
  private float blockCachePercentMaxRange;

  private static long AM_FILE_POINTER = 0;
  private static long RS_FILE_POINTER = 0;
  private static long DN_FILE_POINTER = 0; 
  private static long NN_FILE_POINTER = 0;

  private static RandomAccessFile allmetricsfile = null; 
  private static RandomAccessFile regionserverlog = null;
  private static RandomAccessFile datanodemetrics = null;
  private static RandomAccessFile namenodemetrics = null;
  private static RandomAccessFile readpropfile = null;

  private static float blocking_period_per_update = 0;
  private static float am_storeFileSize = 0;

  private static float read_prop=0.9f;
  private static float write_prop=0.1f;
 
  public long getBlockCacheEvictionCount(long end) throws Exception {
      boolean first=true;
      long allmetrics_blockCacheEvictionCount_ini = 0;
      long allmetrics_blockCacheEvictionCount_next=0;
      allmetricsfile.seek(AM_FILE_POINTER);
      while(AM_FILE_POINTER < end) {
    	String line = allmetricsfile.readLine();
        Pattern p = Pattern.compile("(\\sblockCacheEvictionCount=)(\\d+),");
        Matcher m = p.matcher(line);
        while(m.find()) {
          if(first) {
            first=false;
            allmetrics_blockCacheEvictionCount_ini=Long.valueOf(m.group(2)).longValue();
          }
          else {
	    allmetrics_blockCacheEvictionCount_next=Long.valueOf(m.group(2)).longValue();
          }
        }

        Pattern p1 = Pattern.compile("(\\sstoreFileSize=)([\\d\\.]+),");
        Matcher m1 = p1.matcher(line);
        while(m1.find()) {
            am_storeFileSize = Float.valueOf(m1.group(2)).floatValue()/(1024*1024*1024);
        }

        
        AM_FILE_POINTER = allmetricsfile.getFilePointer();    
      }

      long blocksevicted = allmetrics_blockCacheEvictionCount_next - allmetrics_blockCacheEvictionCount_ini;
      System.out.println("log_evicted_initial: " + allmetrics_blockCacheEvictionCount_ini);
      System.out.println("log_evicted_last: " + allmetrics_blockCacheEvictionCount_next );
      System.out.println("log_evicted_count: " + blocksevicted);
      System.out.println("storeFileSize: " + am_storeFileSize);
      return(blocksevicted);
  }

  public float getCapacityUsed(long end) throws Exception {
      float nn_capacityused = 0;
      namenodemetrics.seek(NN_FILE_POINTER);
      while(NN_FILE_POINTER < end) {
    	String line = namenodemetrics.readLine();
        Pattern p = Pattern.compile("(\\sCapacityUsedGB=)([\\d\\.]+),");
        Matcher m = p.matcher(line);
        while(m.find()) {
	    nn_capacityused = Float.valueOf(m.group(2)).floatValue();
        }
        NN_FILE_POINTER = namenodemetrics.getFilePointer();    
      }
      System.out.println("selfdapql capacity used: " + nn_capacityused);
      return(nn_capacityused);
  }

  public float getAvgReadTime(long end)  throws Exception {
    float total_ops_time = 0.0f;
    long total_ops = 0;
    long ops_ini=0;
    long ops_next=0;
    long ops_last=0;
    boolean first = true;
    datanodemetrics.seek(DN_FILE_POINTER);
     while(DN_FILE_POINTER < end) {
      String line = datanodemetrics.readLine();
      Pattern p = Pattern.compile("(\\sReadBlockOpNumOps=)(\\d+),(\\sReadBlockOpAvgTime=)([\\d\\.]+),");
      Matcher m = p.matcher(line);
      while(m.find()) {
        float local_avg_time =  Float.valueOf(m.group(4)).floatValue();
        if(first) {
          first = false;
          ops_ini = Long.valueOf(m.group(2)).longValue();
          ops_next = ops_ini;
        }
        else {
          ops_next = Long.valueOf(m.group(2)).longValue();
          long delta_ops = ops_next - ops_last;
          total_ops_time = total_ops_time + delta_ops * local_avg_time;
        }
        ops_last = ops_next;
      }
      DN_FILE_POINTER = datanodemetrics.getFilePointer();
    } 
    total_ops = ops_next - ops_ini;
    float total_avg_time = 0.0f;
    if(total_ops != 0) 
    {
        total_avg_time = total_ops_time/(float)total_ops;
    }
    System.out.println("selfdapql total operation time: " + total_ops_time);
    System.out.println("selfdapql total # operations: " + total_ops);
    System.out.println("selfdapql dfs avg read time: " + total_avg_time);
    return (total_avg_time);  
  }

  public long getBlockingUpdatesCount(long end)  throws Exception{
    long blocking_updates_count=0;
    long total_blocking_time=0;
    regionserverlog.seek(RS_FILE_POINTER);
    while(RS_FILE_POINTER < end) {
      String line = regionserverlog.readLine();
      Pattern p = Pattern.compile("Blocking updates");
      Matcher m = p.matcher(line);
      while(m.find()) {
        blocking_updates_count++;
      } 
      Pattern t = Pattern.compile("Memstore is above high water mark and block (\\d+)ms");
      Matcher tm = t.matcher(line);
      while(tm.find()) {
        total_blocking_time = total_blocking_time + Long.valueOf(tm.group(1)).longValue();
      }
      RS_FILE_POINTER = regionserverlog.getFilePointer(); 
    }
    if(blocking_updates_count==0) {
      blocking_period_per_update = 0;
    }
    else {
      blocking_period_per_update = ((float)total_blocking_time)/blocking_updates_count;
    }
    System.out.println("selfdapql blocking update blocking_updates_count: " + blocking_updates_count);
    System.out.println("selfdapql blocking update avg total_blocking_time: " + blocking_period_per_update);
    return blocking_updates_count;
  }
 
  @Override
  public TunerResult tune(TunerContext context) {
      long am_blockCacheEvictionCount=0;
      long rslog_blocking_updates_count=0;
      float dnmetrics_avg_read_time=0;
      float nnmetrics_capacity_used=0;
    try {
      allmetricsfile = new RandomAccessFile("/home/hadoop/hbase/all.metrics", "r");
      regionserverlog = new RandomAccessFile("/home/hadoop/hbase/logs/regionserverlog", "r");
      datanodemetrics = new RandomAccessFile("/home/hadoop/hadoop/datanode-metrics.out", "r");
      //namenodemetrics = new RandomAccessFile("/home/hadoop/hadoop/namenode-metrics.out", "r");
      long am_filelength = allmetricsfile.length();
      if(AM_FILE_POINTER > am_filelength) {
	System.out.println("selfdapql all metrics rolled");
	AM_FILE_POINTER=0;
      }
      System.out.println("----------------------------------------------------------"); 
      System.out.println("selfdapql AM_FILE_POINTER in begining: " + AM_FILE_POINTER);
      System.out.println("selfdapql filelengh: " + am_filelength); 
     
      am_blockCacheEvictionCount = getBlockCacheEvictionCount(am_filelength);
    
      System.out.println("selfdapql AM_FILE_POINTER in end: " + AM_FILE_POINTER);
      // counting the blocking updates in regionserver log
      long rs_filelength = regionserverlog.length();
      if(RS_FILE_POINTER > rs_filelength) {
        System.out.println("selfdapql log rolled");
        RS_FILE_POINTER=0;
      }

      System.out.println("selfdapql RS_FILE_POINTER in begining: " + RS_FILE_POINTER);
      System.out.println("selfdapql rs_filelengh: " + rs_filelength);

      rslog_blocking_updates_count = getBlockingUpdatesCount(rs_filelength);

      System.out.println("selfdapql RS_FILE_POINTER in end: " + RS_FILE_POINTER);
      // measuring the dfs_avg_time
      long dn_filelength = datanodemetrics.length();
      if(DN_FILE_POINTER > dn_filelength) {
        System.out.println("selfdapql datanode metrics rolled");
	DN_FILE_POINTER=0;
      }      
      
      System.out.println("selfdapql DN_FILE_POINTER in begining: " + DN_FILE_POINTER);
      System.out.println("selfdapql dn_filelength: " + dn_filelength);

      dnmetrics_avg_read_time = getAvgReadTime(dn_filelength);

      System.out.println("selfdapql DN_FILE_POINTER in end: " + DN_FILE_POINTER);

      //long nn_filelength = namenodemetrics.length();
      //if(NN_FILE_POINTER > nn_filelength) {
      //  System.out.println("selfdapql namenode metrics rolled");
      // NN_FILE_POINTER=0;
      //}

      //System.out.println("selfdapql NN_FILE_POINTER in begining: " + NN_FILE_POINTER);
      //System.out.println("selfdapql nn_filelength: " + nn_filelength);

      //nnmetrics_capacity_used = getCapacityUsed(nn_filelength);

      //System.out.println("selfdapql NN_FILE_POINTER in end: " + NN_FILE_POINTER);
 


      allmetricsfile.close();
      regionserverlog.close();
      datanodemetrics.close();
    }
    catch(Exception ex) {
      ex.printStackTrace();
    }

    long blockedFlushCount = rslog_blocking_updates_count;
    long unblockedFlushCount = context.getUnblockedFlushCount();
    long evictCount = am_blockCacheEvictionCount;
    boolean memstoreSufficient = blockedFlushCount == 0 && unblockedFlushCount == 0;
    boolean blockCacheSufficient = evictCount == 0;
    if (memstoreSufficient && blockCacheSufficient) {
      return NO_OP_TUNER_RESULT;
    }
    float newMemstoreSize;
    float newBlockCacheSize;
    if (memstoreSufficient) {
      // Increase the block cache size and corresponding decrease in memstore size
      newBlockCacheSize = context.getCurBlockCacheSize() + step;
      newMemstoreSize = context.getCurMemStoreSize() - step;
    } else if (blockCacheSufficient) {
	     // Increase the memstore size and corresponding decrease in block cache size
      newBlockCacheSize = context.getCurBlockCacheSize() - step;
      newMemstoreSize = context.getCurMemStoreSize() + step;
    } else {
      return NO_OP_TUNER_RESULT;
      // As of now not making any tuning in write/read heavy scenario.
    }
    
    if (newMemstoreSize > globalMemStorePercentMaxRange) {
       newMemstoreSize = globalMemStorePercentMaxRange;
    } else if (newMemstoreSize < globalMemStorePercentMinRange) {
       newMemstoreSize = globalMemStorePercentMinRange;
    }  
    if (newBlockCacheSize > blockCachePercentMaxRange) {
      newBlockCacheSize = blockCachePercentMaxRange;
    } else if (newBlockCacheSize < blockCachePercentMinRange) {
      newBlockCacheSize = blockCachePercentMinRange;
    }
    TUNER_RESULT.setBlockCacheSize(newBlockCacheSize);
    TUNER_RESULT.setMemstoreSize(newMemstoreSize);
    System.out.println("selfdapql newBlockCacheSize: " + newBlockCacheSize);
    System.out.println("selfdapql newMemstoreSize: " + newMemstoreSize);
    return TUNER_RESULT;
  }

  @Override
  public Configuration getConf() {
    return this.conf;
  }

  @Override
  public void setConf(Configuration conf) {
    this.conf = conf;
    this.step = conf.getFloat(STEP_KEY, DEFAULT_STEP_VALUE);
    this.blockCachePercentMinRange = conf.getFloat(BLOCK_CACHE_SIZE_MIN_RANGE_KEY,
        conf.getFloat(HFILE_BLOCK_CACHE_SIZE_KEY, HConstants.HFILE_BLOCK_CACHE_SIZE_DEFAULT));
    this.blockCachePercentMaxRange = conf.getFloat(BLOCK_CACHE_SIZE_MAX_RANGE_KEY,
        conf.getFloat(HFILE_BLOCK_CACHE_SIZE_KEY, HConstants.HFILE_BLOCK_CACHE_SIZE_DEFAULT));
    this.globalMemStorePercentMinRange = conf.getFloat(MEMSTORE_SIZE_MIN_RANGE_KEY,
        MemStoreFlusher.getGlobalMemStorePercent(conf));
    this.globalMemStorePercentMaxRange = conf.getFloat(MEMSTORE_SIZE_MAX_RANGE_KEY,
        MemStoreFlusher.getGlobalMemStorePercent(conf));
  }

  public static void main(String[] args) {
    System.out.println("Testing");
  }
}

